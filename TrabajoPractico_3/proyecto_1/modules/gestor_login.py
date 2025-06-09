from flask_login import UserMixin
from flask_login import login_user, logout_user, login_required, current_user
from flask import abort
from functools import wraps

class FlaskLoginUser(UserMixin):
    def __init__(self, dicc_usuario):
        self.id = dicc_usuario["id"]
        self.nombre = dicc_usuario["nombre"]
        self.email = dicc_usuario["email"]
        self.password = dicc_usuario["password"]
        self.rol= dicc_usuario["rol"]
        self.departamento= dicc_usuario.get("departamento", "sin_departamento")

    def es_jefe(self):
        return self.rol == "jefe"

    def es_secretario(self):
        return self.rol == "secretario"

    def es_tecnico(self):
        return self.rol == "tecnico"
    
class GestorDeLogin:
    def __init__(self, gestor_usuarios, login_manager, admin_list):
        self.__gestor_usuarios = gestor_usuarios
        login_manager.user_loader(self.__cargar_usuario_actual)
        self.__admin_list = admin_list

    @property
    def nombre_usuario_actual(self):
        return current_user.nombre

    @property
    def id_usuario_actual(self):
        return current_user.id
    
    @property
    def usuario_autenticado(self):
        return current_user.is_authenticated

    def __cargar_usuario_actual(self, id_usuario):
        dicc_usuario = self.__gestor_usuarios.cargar_usuario(id_usuario)
        if dicc_usuario is None:
            return None
        return FlaskLoginUser(dicc_usuario)
    
    def login_usuario(self, dicc_usuario):
        user = FlaskLoginUser(dicc_usuario)
        login_user(user)
        print(f"Usuario {current_user.nombre} ha iniciado sesión")

    def logout_usuario(self):
        logout_user()
        print("Usuario ha cerrado sesión")
        print(f"Usuario actual {current_user}")

    def admin_only(self, f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if current_user.is_authenticated and current_user.id not in self.__admin_list:
                return abort(403)
            return f(*args, **kwargs)
        return decorated_function
    
    def se_requiere_login(self, func):
        return login_required(func)
    
    def es_admin(self):
        if current_user.is_authenticated and current_user.id in self.__admin_list:
            return True
        else:
            return False
        
