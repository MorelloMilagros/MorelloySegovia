from flask import Flask, render_template, request,flash, redirect, url_for, session, Response
from flask_login import LoginManager, login_required, current_user
from modules.config import app, login_manager
from modules.factoria import crear_repositorio
from modules.gestor_login import GestorDeLogin
from modules.gestor_reclamos import GestorDeReclamos
from modules.gestor_usuarios import GestorDeUsuarios
from modules.formularios import FormRegistro, FormLogin, FormReclamo
from modules.graficador_concreto import GraficadorMatplotlib
from modules.analitica import Analitica
from werkzeug.utils import secure_filename
import pickle
import os

with open('./data/claims_clf.pkl', 'rb') as archivo:
    clasificador = pickle.load(archivo)

#Configuración básica de Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'clave_12332141'
app.config["UPLOAD_FOLDER"] = "static/uploads"


login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view= "login"

@login_manager.user_loader
def load_user(user_id):
    usuario = gestor_usuarios.cargar_usuario(user_id)
    return usuario
    """
    Carga un usuario desde la base de datos para Flask-Login.

    Esta función es un callback requerido por Flask-Login. Se utiliza para recargar el objeto
    de usuario a partir del ID de usuario almacenado en la sesión.

    Args:
        user_id (str): El ID del usuario a cargar.

    Returns:
        FlaskLoginUser or None: Una instancia de `FlaskLoginUser` si el usuario existe, de lo contrario, `None`.
    """
#Crear repositorios y gestores
admin_list = [1]
repo_reclamos, repo_usuarios = crear_repositorio()
gestor_usuarios = GestorDeUsuarios(repo_usuarios)
gestor_reclamos = GestorDeReclamos(repo_reclamos, clasificador)
gestor_login = GestorDeLogin(gestor_usuarios, login_manager, admin_list)
graficador = GraficadorMatplotlib()
analitica_fachada = Analitica(gestor_reclamos, graficador)
# Página de inicio
@app.route('/')
def inicio():
    """Pagina de inicio con con navegacion a funciones"""
    if 'username' in session and gestor_login.usuario_autenticado:
        return redirect(url_for('listar_reclamos'))
    session['username'] = 'Invitado'
    lista_reclamos= gestor_reclamos.listar_reclamos()
    return render_template('inicio.html', user=session['username'], lista_reclamos=lista_reclamos)
    """
    Muestra la página de inicio de la aplicación.

    Si el usuario ya está autenticado, lo redirige a la lista de reclamos
    (o a su menú principal si es un usuario normal). De lo contrario,
    muestra la página de bienvenida con opciones para registrarse o iniciar sesión.

    Returns:
        render_template: La plantilla 'inicio.html' o una redirección.
    """

@app.route('/register', methods=['GET', 'POST'])
def register():
    form_registro= FormRegistro()
    if form_registro.validate_on_submit():
        try:
            gestor_usuarios.registrar_nuevo_usuario(form_registro.nombre.data,
                                                     form_registro.apellido.data,
                                                     form_registro.username.data,
                                                     form_registro.email.data,
                                                     form_registro.password.data,
                                                     form_registro.claustro.data)
        except ValueError as e:
            flash(str(e), "error")
        else:
            flash("Usuario registrado exitosamente", "success")
            return redirect(url_for("login"))
    return render_template('registro.html', form=form_registro)

    """
    Maneja el registro de nuevos usuarios en el sistema.

    - **GET**: Muestra el formulario de registro.
    - **POST**: Procesa los datos enviados por el formulario. Valida los datos
      (usando Flask-WTF) y, si son válidos, intenta registrar al usuario
      a través del `GestorDeUsuarios`. Si el registro es exitoso, redirige
      al login; de lo contrario, muestra mensajes de error.

    Returns:
        render_template: La plantilla 'registro.html' con el formulario.
        redirect: Redirección a la página de login en caso de éxito.
    """

@app.route('/login', methods=['GET', 'POST'])
def login():
    form_login= FormLogin()
    if form_login.validate_on_submit():
        try:
            usuario=gestor_usuarios.autenticar_usuario(form_login.email.data, form_login.password.data)
            gestor_login.login_usuario(usuario)
            session['username']= gestor_login.nombre_usuario_actual
            if current_user.es_jefe() or current_user.es_secretario(): # Simplificado
                return redirect(url_for('dashboard'))
            else:
                return redirect(url_for('menu_principal'))
        except ValueError as e:
            flash(str(e), "error")
    return render_template('login.html', form=form_login)
    """
    Maneja el inicio de sesión de usuarios existentes.

    - **GET**: Muestra el formulario de login.
    - **POST**: Procesa las credenciales enviadas. Intenta autenticar al usuario
      mediante el `GestorDeUsuarios`. Si la autenticación es exitosa, inicia
      la sesión con Flask-Login y redirige al usuario a su panel correspondiente
      (dashboard para jefes/secretarios, menú principal para usuarios comunes).
      Si falla, muestra un mensaje de error.

    Returns:
        render_template: La plantilla 'login.html' con el formulario.
        redirect: Redirección al dashboard o menú principal en caso de éxito.
    """
@app.route('/menu_principal')
@login_required
def menu_principal():
    """Menú principal que muestra las opciones principales al usuario."""
    return render_template("menu_principal.html")
"""
Muestra el menú principal para los usuarios finales.
Requiere que el usuario esté autenticado (`@login_required`).
Returns:
render_template: La plantilla 'menu_principal.html'.
    """
@app.route('/logout')
@login_required
def logout():
    gestor_login.logout_usuario()
    session['username'] = 'Invitado'
    return redirect(url_for('inicio'))
    """
    Cierra la sesión del usuario actual.

    Invalida la sesión de Flask-Login y redirige al usuario a la página de inicio.

    Returns:
        redirect: Redirección a la página de inicio.
    """
@app.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    """Panel exclusivo para jefes y secretarios"""
    if not(current_user.es_jefe() or current_user.es_secretario()):
        flash("Acceso denegado", "error")
        return redirect(url_for('inicio'))
    try:
        depto= current_user.departamento
        reclamos, stats = analitica_fachada.obtener_datos_dashboard(departamento=depto)
    except Exception as e:
        flash(f"Error cargando datos del dashboard: {str(e)}", "error")
        reclamos=[]
        stats={}

    return render_template('dashboard.html', lista_reclamos=reclamos, stats=stats)
    """
    Muestra el panel de administración para jefes de departamento y secretarios.

    Requiere que el usuario esté autenticado y que tenga el rol de 'jefe' o 'secretario'.
    Si el usuario no tiene el rol adecuado, se deniega el acceso.
    Muestra una lista de reclamos del departamento del usuario y estadísticas relevantes.

    Returns:
        render_template: La plantilla 'dashboard.html' con los reclamos y estadísticas.
        redirect: Redirección a la página de inicio si el acceso es denegado.
    """
@app.route('/derivar/<int:id>', methods=['GET', 'POST'])
@login_required
def derivar_reclamo(id):
    """
    Permite al Secretario Técnico derivar un reclamo a otro departamento.
    """
    # 1. Verificar permisos
    if not current_user.es_secretario():
        flash("Acceso denegado. Solo la Secretaría Técnica puede derivar reclamos.", "error")
        return redirect(url_for('dashboard'))

    # 2. Obtener datos necesarios
    reclamo = gestor_reclamos.obtener_reclamo(id)
    if not reclamo:
        flash("Reclamo no encontrado.", "error")
        return redirect(url_for('dashboard'))

    # 3. Manejar la solicitud POST (cuando se confirma la derivación)
    if request.method == 'POST':
        nuevo_departamento = request.form.get('nuevo_departamento')
        try:
            gestor_reclamos.derivar_reclamo(id, nuevo_departamento)
            flash(f"Reclamo {id} derivado exitosamente a {nuevo_departamento}.", "success")
            return redirect(url_for('dashboard'))
        except ValueError as e:
            flash(str(e), "error")

    # 4. Manejar la solicitud GET (mostrar la página para derivar)
    departamentos = gestor_reclamos.obtener_departamentos()
    return render_template('derivar_reclamo.html', reclamo=reclamo, departamentos=departamentos)
    
@app.route('/listar_reclamos', methods=['GET'])
@login_required
def listar_reclamos():
    """Lista todos los reclamos disponibles."""
    departamento_filtro = request.args.get('departamento')

    if current_user.es_jefe() or current_user.es_secretario():
        lista_reclamos = gestor_reclamos.listar_reclamos_por_departamento(current_user.departamento)
    else:
        if departamento_filtro:
            lista_reclamos = gestor_reclamos.listar_reclamos_por_departamento(departamento_filtro, estado="pendiente")
        else:
            lista_reclamos = gestor_reclamos.listar_reclamos_para_usuarios()
            
    departamentos = gestor_reclamos.obtener_departamentos()

    return render_template('listar_reclamos.html', 
                          lista_reclamos=lista_reclamos, 
                          departamentos=departamentos, 
                          departamento_filtro=departamento_filtro)
    """
    Lista todos los reclamos disponibles o filtra por departamento.

    Permite a los usuarios generales ver reclamos pendientes (con opción de filtrar
    por departamento). Los usuarios con rol de personal (jefe/secretario/técnico)
    ven todos los reclamos de su propio departamento, sin la opción de filtro general.

    Args:
        departamento (str, opcional): El departamento por el cual filtrar los reclamos.
                                       Se obtiene de los parámetros de la URL.

    Returns:
        render_template: La plantilla 'listar_reclamos.html' con la lista de reclamos
                         y los departamentos disponibles para filtrar.
    """

@app.route("/agregar_reclamo", methods=["GET", "POST"])
@login_required
def agregar_reclamo():
    """Formulario para crear un reclamo nuevo."""
    form_reclamo = FormReclamo()
    departamentos_disponibles= gestor_reclamos.obtener_departamentos()
    form_reclamo.departamento.choices=[(d,d) for d in departamentos_disponibles]

    descripcion = form_reclamo.descripcion.data or request.form.get("descripcion")
    departamento = form_reclamo.departamento.data or request.form.get("departamento")
    id_usuario = int(current_user.id)  

    foto_archivo=form_reclamo.foto.data
    nombre_archivo= None

    if foto_archivo:
        nombre_archivo= secure_filename(foto_archivo.filename)
        ruta_archivo= os.path.join(app.config["UPLOAD_FOLDER"], nombre_archivo)
        foto_archivo.save(ruta_archivo)
    if request.method == "POST":
        if not descripcion or not departamento:
            flash("Faltan datos: descripción o departamento", "error")
            return redirect(url_for("agregar_reclamo"))

        reclamos_similares = gestor_reclamos.buscar_similares(descripcion)
        if reclamos_similares and "descripcion" not in request.form:
            return render_template("reclamos_similares.html",
                                  similares=reclamos_similares,
                                  descripcion=descripcion,
                                  departamento=departamento,
                                  nombre_archivo=nombre_archivo)
        try:
            gestor_reclamos.agregar_nuevo_reclamo(descripcion, id_usuario, departamento, p_foto=nombre_archivo)
            flash("Reclamo agregado con éxito", "success")
            return redirect(url_for("listar_reclamos"))
        except Exception as e:  
            flash(f"Error al crear el reclamo: {str(e)}", "error ")

    return render_template("agregar_reclamo.html", form=form_reclamo)
    """
    Permite a un usuario crear un nuevo reclamo.

    - **GET**: Muestra el formulario para crear el reclamo, precargando los
      departamentos disponibles.
    - **POST**: Procesa los datos del formulario. Si se detectan reclamos
      similares basados en la descripción, ofrece la opción de adherirse
      a uno existente. Si no hay similares o el usuario elige crear uno nuevo,
      el reclamo se guarda en la base de datos. También maneja la subida de fotos
      adjuntas al reclamo.

    Muestra mensajes de éxito o error al usuario.

    Returns:
        render_template: Las plantillas 'agregar_reclamo.html' o 'reclamos_similares.html'.
        redirect: Redirección a la lista de reclamos en caso de éxito.
    """

@app.route('/adherirse', methods=['POST'])
@login_required
def adherirse():
    id_reclamo= request.form.get("id_reclamo")
    try:
        gestor_reclamos.adherir_a_reclamo(current_user.id, int(id_reclamo))
        flash("Te adheriste al reclamo", "success")
    except ValueError as e:
        flash(str(e), "error")
    return redirect(url_for("listar_reclamos"))
    """
    Permite a un usuario adherirse a un reclamo existente.

    Recibe el ID del reclamo al que adherirse desde un formulario POST.
    Llama al gestor de reclamos para registrar la adhesión y muestra un mensaje
    de éxito o error.

    Returns:
        redirect: Redirección a la página de listar reclamos después de la operación.
    """
@app.route('/mis_reclamos')
@login_required
def mis_reclamos():
    """"Ver reclamos del propio usuario"""
    usuario_id=int(current_user.id)
    todos=gestor_reclamos.repo.obtener_todos_los_registros()
    propios= [r for r in todos if r.id_usuario ==usuario_id]
    return render_template("mis_reclamos.html", lista_reclamos=propios)
    """
    Muestra la lista de reclamos creados por el usuario actual.

    Filtra todos los reclamos para mostrar solo aquellos cuyo `id_usuario`
    coincide con el ID del usuario autenticado.

    Returns:
        render_template: La plantilla 'mis_reclamos.html' con la lista de reclamos del usuario.
    """
@app.route("/edit", methods=['GET', 'POST'])
@login_required
def editar_reclamo():
    """Editar el estado de un reclamo existente."""
    id_reclamo = request.args.get('id')
    reclamo = gestor_reclamos.obtener_reclamo(id_reclamo)

    if request.method == "POST":
        nuevo_estado = request.form.get("estado")
        dias_str = request.form.get("tiempo")
        
        # Verificación temprana para una mejor experiencia de usuario
        if nuevo_estado == "en proceso" and not dias_str:
            flash("Para poner un reclamo 'en proceso', debes especificar un tiempo de resolución.", "error")
            return render_template("editar_reclamo.html", reclamo=reclamo)

        try:
            # Convertimos a entero solo si existe
            dias_int = int(dias_str) if dias_str else None
            
            gestor_reclamos.actualizar_estado_reclamo(id_reclamo, nuevo_estado, dias_int)
            flash("Reclamo actualizado con éxito.", "success")
            return redirect(url_for("dashboard"))
        except ValueError as e:
            # El gestor ahora nos da errores más claros, que le mostramos al usuario
            flash(str(e), "error")
            return render_template("editar_reclamo.html", reclamo=reclamo)
    
    return render_template("editar_reclamo.html", reclamo=reclamo)
    """
    Permite a un jefe de departamento o secretario editar el estado de un reclamo.

    - **GET**: Muestra el formulario de edición para un reclamo específico (identificado por ID en la URL).
    - **POST**: Procesa la actualización del estado del reclamo. Si el nuevo estado es
      "en proceso", requiere un tiempo de resolución en días (entre 1 y 15).
      Muestra mensajes de éxito o error.

    Returns:
        render_template: La plantilla 'editar_reclamo.html' con los detalles del reclamo.
        redirect: Redirección al dashboard después de una actualización exitosa.
    """
@app.route('/analitica')
@login_required
def analitica():
    if not (current_user.es_jefe() or current_user.es_secretario()):
        flash("Acceso no permitido")
        return redirect(url_for('inicio'))
    depto=current_user.departamento
    _, stats = analitica_fachada.obtener_datos_dashboard(departamento=depto)
    return render_template("analitica.html", stats=stats, departamento=depto)
    """
    Muestra las estadísticas y gráficos de los reclamos para el departamento
    del usuario autenticado (jefe o secretario).

    Requiere que el usuario tenga rol de 'jefe' o 'secretario'.
    Obtiene las estadísticas del `GestorDeReclamos`, que incluyen el total de reclamos,
    porcentajes por estado, medianas de tiempo de resolución y las palabras clave más frecuentes.

    Returns:
        render_template: La plantilla 'analitica.html' con los datos estadísticos.
        redirect: Redirección a la página de inicio si el acceso es denegado.
    """

@app.route('/grafico/<tipo_grafico>/<departamento>')
@login_required
def grafico(tipo_grafico, departamento):
    if not (current_user.es_jefe() or current_user.es_secretario()) or current_user.departamento != departamento:
        return "Acceso denegado", 403
    
    try:
        # La fachada nos da la imagen del gráfico que pidamos
        img_bytes = analitica_fachada.obtener_imagen_grafico(tipo_grafico, departamento)
        if img_bytes is None:
            return "No hay datos para mostrar el gráfico.", 404
        return Response(img_bytes, mimetype='image/png')
    except ValueError as e:
        return str(e), 400 # Error si el tipo de gráfico no es válido
    except Exception as e:
        return f"Error generando el gráfico: {e}", 500
    
@app.route('/ayuda')
@login_required
def ayuda():
    return render_template("ayuda.html")
    """
    Muestra una página de ayuda o tutorial sobre el uso del sistema.

    Es accesible para todos los usuarios logueados.

    Returns:
        render_template: La plantilla 'ayuda.html'.
    """
@app.route('/generar_reporte')
@login_required
def generar_reporte():
    """
    Controlador "delgado". No contiene lógica, solo delega a la fachada.
    """
    if not(current_user.es_jefe() or current_user.es_secretario()):
        flash("Acceso denegado.", "error")
        return redirect(url_for('inicio'))

    formato = request.args.get('formato', 'html').lower()
    departamento = current_user.departamento
    
    try:
        # 1. Se delega TODO el trabajo a la fachada
        output, mimetype, headers = analitica_fachada.generar_reporte_formateado(departamento, formato)
        
        # 2. Se envía la respuesta que la fachada preparó
        return Response(output, mimetype=mimetype, headers=headers)

    except ValueError as e: # Captura el error si el formato no es válido
        flash(str(e), "error")
        return redirect(url_for('dashboard'))
    except Exception as e: # Captura cualquier otro error en la generación
        flash(f"Error al generar el reporte: {e}", "error")
        return redirect(url_for('dashboard'))
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)

