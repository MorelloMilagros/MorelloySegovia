# Ejemplo de aplicación principal en Flask
from flask import Flask, render_template, request, jsonify,flash, redirect, url_for, session
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from modules.config import app, login_manager
from modules.monticulo_binario import MonticuloBinarioMax, MonticuloBinarioMin
from modules.factoria import crear_repositorio
from modules.gestor_login import GestorDeLogin
from modules.gestor_reclamos import GestorDeReclamos
from modules. gestor_usuarios import GestorDeUsuarios
from modules.formularios import FormRegistro, FormLogin

#Configuración básica de Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'clave_12332141'

login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view= "login"

@login_manager.user_loader
def load_user(user_id):
    return gestor_usuarios.cargar_usuario(user_id)

#Crear repositorios y gestores
admin_list = [1]
repo_reclamos, repo_usuarios = crear_repositorio()
gestor_usuarios = GestorDeUsuarios(repo_usuarios)
gestor_reclamos = GestorDeReclamos(repo_reclamos)
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

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    form_registro= FormRegistro()
    if form_registro.validate_on_submit():
        try:
            gestor_usuarios.registrar_nuevo_usuario(form_registro.nombre.data, form_registro.email.data, form_registro.password.data)
            flash("Usuario registrado exitosamente")
            return redirect(url_for("login"))
        except ValueError as e:
            flash(str(e))
    return render_template('registro.html', form=form_registro)

@app.route('/login')
def login():
    form_login= FormLogin()
    if form_login.validate_on_submit():
        try:
            usuario=gestor_usuarios.autenticar_usuario(form_login.email.data, form_login.password.data)
            login_user(usuario)
            session['username']= usuario.nombre
            return redirect(url_for('listar_reclamos'))
        except ValueError as e:
            flash(str(e))
    return render_template('login.html', form=form_login)

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
    if not(current_user.es_jefe() or current_user.es_secretario):
        return  redirect(url_for('inicio'))
    return render_template('dashboard.html')

@app.route('/listar', methods=['GET'])
@login_required
def listar_reclamos():
    """Lista todos los reclamos disponibles."""
    lista_reclamos= gestor_reclamos.listar_reclamos()
    return render_template('listar_reclamos.html', lista_reclamos=lista_reclamos)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)

