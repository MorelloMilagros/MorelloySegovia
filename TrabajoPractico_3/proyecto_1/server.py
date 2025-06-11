from flask import Flask, render_template, request,flash, redirect, url_for, session, Response
from flask_login import LoginManager, login_required, logout_user, current_user
from modules.config import app, login_manager
from modules.factoria import crear_repositorio
from modules.gestor_login import GestorDeLogin
from modules.gestor_reclamos import GestorDeReclamos
from modules. gestor_usuarios import GestorDeUsuarios
from modules.formularios import FormRegistro, FormLogin, FormReclamo
from modules.dominio import Usuario
from datetime import datetime
from werkzeug.utils import secure_filename
from io import BytesIO             
from xhtml2pdf import pisa   
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
    usuario= gestor_usuarios.cargar_usuario(user_id)
    if isinstance(usuario, dict):  # Si es un diccionario, convierte en objeto Usuario
        usuario = Usuario(usuario["id"], usuario["nombre"], usuario["email"], usuario["password"], usuario["rol"])

    return usuario
#Crear repositorios y gestores
admin_list = [1]
repo_reclamos, repo_usuarios = crear_repositorio()
gestor_usuarios = GestorDeUsuarios(repo_usuarios)
gestor_reclamos = GestorDeReclamos(repo_reclamos, clasificador)
gestor_login= GestorDeLogin(gestor_usuarios, login_manager, admin_list)


# Página de inicio
@app.route('/')
def inicio():
    """Pagina de inicio con con navegacion a funciones"""
    if 'username' in session and gestor_login.usuario_autenticado:
        return redirect(url_for('listar_reclamos'))
    session['username'] = 'Invitado'
    lista_reclamos= gestor_reclamos.listar_reclamos()
    return render_template('inicio.html', user=session['username'], lista_reclamos=lista_reclamos)

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

@app.route('/login', methods=['GET', 'POST'])
def login():
    form_login= FormLogin()
    if form_login.validate_on_submit():
        try:
            usuario=gestor_usuarios.autenticar_usuario(form_login.email.data, form_login.password.data)
            gestor_login.login_usuario(usuario)
            session['username']= gestor_login.nombre_usuario_actual
            if current_user.es_jefe() or current_user.es_secretario or current_user.es_tecnico():
                return redirect(url_for('dashboard'))
            else:
                        return redirect(url_for('menu_principal'))
        except ValueError as e:
                    flash(str(e), "error")
    return render_template('login.html', form=form_login)

@app.route('/menu_principal')
@login_required
def menu_principal():
    """Menú principal que muestra las opciones principales al usuario."""
    return render_template("menu_principal.html")

@app.route('/logout')
@login_required
def logout():
    logout_user()
    session['username'] = 'Invitado'
    return redirect(url_for('inicio'))

@app.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    """Panel exclusivo para jefes y secretarios"""
    if not(current_user.es_jefe() or current_user.es_secretario() or current_user.es_tecnico()):
        flash("Acceso denegado", "error")
        return  redirect(url_for('inicio'))
    try:
        reclamos= gestor_reclamos.listar_reclamos_por_departamento(current_user.departamento)
        stats=gestor_reclamos.obtener_estadisticas(current_user.departamento)
    except Exception as e:
        flash(f"Error cargando datos del dashboard: {str(e)}", "error")
        reclamos=[]
        stats={}

    return render_template('dashboard.html', lista_reclamos=reclamos, stats=stats)

@app.route('/listar_reclamos', methods=['GET'])
@login_required
def listar_reclamos():
    """Lista todos los reclamos disponibles."""
    departamento_filtro = request.args.get('departamento')

    if current_user.es_jefe() or current_user.es_secretario() or current_user.es_tecnico():
        # Los jefes ven todos los estados de su depto.
        lista_reclamos = gestor_reclamos.listar_reclamos_por_departamento(current_user.departamento)
    else:
        # Los usuarios finales solo ven reclamos "pendientes"
        if departamento_filtro:
            # Filtra por departamento, pero solo los pendientes
            lista_reclamos = gestor_reclamos.listar_reclamos_por_departamento(departamento_filtro, estado="pendiente")
        else:
            # Muestra todos los pendientes de todos los deptos.
            lista_reclamos = gestor_reclamos.listar_reclamos_para_usuarios()
            
    departamentos = gestor_reclamos.obtener_departamentos()

    return render_template('listar_reclamos.html', 
                           lista_reclamos=lista_reclamos, 
                           departamentos=departamentos, 
                           departamento_filtro=departamento_filtro)


@app.route("/agregar_reclamo", methods=["GET", "POST"])
@login_required
def agregar_reclamo():
    """Formulario para crear un reclamo nuevo."""
    form_reclamo = FormReclamo()
    #Se Cargan de forma dinamica los departamentos
    departamentos_disponibles= gestor_reclamos.obtener_departamentos()
    form_reclamo.departamento.choices=[(d,d) for d in departamentos_disponibles]

    #Obtener descripción y departamento de cualquiera de los dos caminos
    descripcion = form_reclamo.descripcion.data or request.form.get("descripcion")
    departamento = form_reclamo.departamento.data or request.form.get("departamento")
    id_usuario = int(current_user.id)  

    #Manejo de la imagen del reclamo
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

        #Buscar reclamos similares
        reclamos_similares = gestor_reclamos.buscar_similares(descripcion)
        if reclamos_similares and "descripcion" not in request.form:
            # Mostrar pantalla para elegir si adherirse o continuar
            return render_template("reclamos_similares.html",
                                   similares=reclamos_similares,
                                   descripcion=descripcion,
                                   departamento=departamento,
                                   nombre_archivo=nombre_archivo)

        #Crear el reclamo si el usuario decide continuar
        try:
            gestor_reclamos.agregar_nuevo_reclamo(descripcion, id_usuario, departamento, p_foto=nombre_archivo)
            flash("Reclamo agregado con éxito", "success")
            return redirect(url_for("listar_reclamos"))
        except Exception as e:  
            flash(f"Error al crear el reclamo: {str(e)}", "error ")

    return render_template("agregar_reclamo.html", form=form_reclamo)


@app.route('/adherirse', methods=['POST'])
@login_required
def adherirse():
    id_reclamo= request.form.get("id_reclamo")
    try:
        gestor_reclamos.adherir_a_reclamo(current_user.id, int(id_reclamo))
        flash("Te adheriste al reclamo", "succes")
    except ValueError as e:
        flash(str(e), "error")
    return redirect(url_for("listar_reclamos"))

@app.route('/mis_reclamos')
@login_required
def mis_reclamos():
    """"Ver reclamos del propio usuario"""
    usuario_id=int(current_user.id)
    todos=gestor_reclamos.repo.obtener_todos_los_registros()
    propios= [r for r in todos if r.id_usuario ==usuario_id]
    return render_template("mis_reclamos.html", listar_reclamos=propios)

@app.route("/edit", methods=['GET', 'POST'])
@login_required
def editar_reclamo():
    """Editar el estado de un reclamo existente."""
    id_reclamo = request.args.get('id')
    reclamo = gestor_reclamos.obtener_reclamo(id_reclamo)

    if request.method == "POST":
        nuevo_estado = request.form.get("estado")
        dias= request.form.get("tiempo")
        try:
            if nuevo_estado=="en proceso" and dias:
                gestor_reclamos.actualizar_estado_reclamo(id_reclamo, nuevo_estado, int(dias))
            else:
                 gestor_reclamos.actualizar_estado_reclamo(id_reclamo, nuevo_estado)
            flash("Reclamo actualizado")
            return redirect(url_for("dashboard"))
        except ValueError as e:
            flash(str(e))   

    return render_template("editar_reclamo.html", reclamo=reclamo)

@app.route('/analitica')
@login_required
def analitica():
    stats= gestor_reclamos.obtener_estadisticas(current_user.departamento)
    return render_template("analitica.html", stats=stats)

@app.route('/ayuda')
@login_required
def ayuda():
    return render_template("ayuda.html")

@app.route('/generar_reporte')
@login_required
def generar_reporte():
    """Genera un reporte de reclamos en formato HTML o PDF usando xhtml2pdf.  """
    # Control de acceso
    if not(current_user.es_jefe() or current_user.es_secretario() or current_user.es_tecnico()):
        flash("Acceso denegado.", "error")
        return redirect(url_for('inicio'))
    try:
        # Obtener los datos 
        departamento = current_user.departamento
        reclamos = gestor_reclamos.listar_reclamos_por_departamento(departamento)
        stats = gestor_reclamos.obtener_estadisticas(departamento)
    except Exception as e:
        flash(f"Error al generar los datos del reporte: {str(e)}", "error")
        return redirect(url_for('dashboard'))

    formato_salida = request.args.get('formato', 'html')

    # Renderiza la plantilla HTML
    html_renderizado = render_template('reporte.html',
                                       lista_reclamos=reclamos,
                                       stats=stats,
                                       departamento=departamento,
                                       fecha_generacion=datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
    if formato_salida == 'pdf':
        # Creamos un buffer de memoria para guardar el PDF
        pdf_buffer = BytesIO()
        
        # Convertimos el HTML a PDF usando pisa
        pisa_status = pisa.CreatePDF(
            BytesIO(html_renderizado.encode('UTF-8')),  # La fuente HTML
            dest=pdf_buffer)                            # El destino donde se guarda el PDF

        # Si la conversión no tuvo errores, enviamos el PDF
        if not pisa_status.err:
            pdf_buffer.seek(0) # Regresamos al inicio del buffer para leer su contenido
            return Response(pdf_buffer,
                            mimetype='application/pdf',
                            headers={'Content-Disposition': 'attachment;filename=reporte_reclamos.pdf'})
        else:
            flash('Hubo un error al generar el archivo PDF.', 'error')
            return redirect(url_for('dashboard'))
    else:
        # Mostrar HTML (sin cambios)
        return html_renderizado

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)

