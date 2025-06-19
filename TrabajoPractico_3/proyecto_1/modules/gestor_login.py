from flask_login import UserMixin
from flask_login import login_user, logout_user, login_required, current_user
from flask import abort
from functools import wraps

class FlaskLoginUser(UserMixin):
    """
    Clase adaptadora para integrar la entidad Usuario con Flask-Login.

    Esta clase toma un diccionario de usuario (típicamente de la base de datos)
    y lo adapta para cumplir con los requisitos de Flask-Login.
    Permite a Flask-Login manejar la sesión del usuario, verificar si está
    autenticado y acceder a sus atributos de forma segura.

    Atributos:
        id (int): El ID único del usuario.
        nombre (str): El nombre del usuario.
        email (str): El email del usuario.
        password (str): La contraseña hasheada del usuario.
        rol (str): El rol del usuario (ej. "usuario", "jefe", "secretario").
        departamento (str): El departamento asociado al usuario, si aplica.
    """
    def __init__(self, dicc_usuario):
        """
        Inicializa una instancia de FlaskLoginUser.

        Args:
            dicc_usuario (dict): Un diccionario que contiene los datos del usuario.
                                 Debe incluir 'id', 'nombre', 'email', 'password',
                                 'rol' y opcionalmente 'departamento'.
        """
        self.id = dicc_usuario["id"]
        self.nombre = dicc_usuario["nombre"]
        self.email = dicc_usuario["email"]
        self.password = dicc_usuario["password"]
        self.rol= dicc_usuario["rol"]
        self.departamento= dicc_usuario.get("departamento", "sin_departamento")

    def es_jefe(self):
        """
        Verifica si el usuario tiene el rol de "jefe".

        Returns:
            bool: True si el rol es "jefe", False en caso contrario.
        """
        return self.rol == "jefe"

    def es_secretario(self):
        """
        Verifica si el usuario tiene el rol de "secretario".

        Returns:
            bool: True si el rol es "secretario", False en caso contrario.
        """
        return self.rol == "secretario"

    def es_tecnico(self):
        """
        Verifica si el usuario tiene el rol de "tecnico".

        Returns:
            bool: True si el rol es "tecnico", False en caso contrario.
        """
        return self.rol == "tecnico"
    
class GestorDeLogin:
    """
    Clase que encapsula la lógica de negocio relacionada con el inicio de sesión
    y la gestión de la sesión de usuarios con Flask-Login.

    Permite autenticar usuarios, iniciar y cerrar sesiones, y proporciona
    decoradores para restringir el acceso a ciertas rutas según el rol.

    Atributos:
        __gestor_usuarios (GestorDeUsuarios): Instancia del gestor de usuarios para cargar datos de usuario.
        __admin_list (list): Lista de IDs de usuario considerados administradores.
    """
    def __init__(self, gestor_usuarios, login_manager, admin_list):
        """
        Inicializa el GestorDeLogin.

        Args:
            gestor_usuarios (GestorDeUsuarios): El gestor de usuarios que se utilizará para
                                                obtener los detalles del usuario.
            login_manager (LoginManager): La instancia de Flask-Login Manager.
            admin_list (list): Una lista de IDs de usuarios que tienen privilegios de administrador.
        """
        self.__gestor_usuarios = gestor_usuarios
        login_manager.user_loader(self.__cargar_usuario_actual)
        self.__admin_list = admin_list

    @property
    def nombre_usuario_actual(self):
        """
        Obtiene el nombre del usuario actualmente autenticado.

        Returns:
            str: El nombre del usuario o una cadena vacía si no hay usuario autenticado.
        """
        return current_user.nombre

    @property
    def id_usuario_actual(self):
        """
        Obtiene el ID del usuario actualmente autenticado.

        Returns:
            int or None: El ID del usuario o None si no hay usuario autenticado.
        """
        return current_user.id
    
    @property
    def usuario_autenticado(self):
        """
        Verifica si hay un usuario actualmente autenticado.

        Returns:
            bool: True si el usuario está autenticado, False en caso contrario.
        """
        return current_user.is_authenticated

    def __cargar_usuario_actual(self, id_usuario):
        """
        Callback interno para Flask-Login: carga el objeto usuario.

        Utiliza el gestor de usuarios para obtener los datos del usuario
        desde la base de datos y crea una instancia de FlaskLoginUser.

        Args:
            id_usuario (str): El ID del usuario a cargar.

        Returns:
            FlaskLoginUser or None: La instancia de FlaskLoginUser si el usuario existe,
                                    o None si no se encuentra.
        """
        dicc_usuario = self.__gestor_usuarios.cargar_usuario(id_usuario)
        if dicc_usuario is None:
            return None
        return FlaskLoginUser(dicc_usuario)
    
    def login_usuario(self, dicc_usuario):
        """
        Inicia la sesión para un usuario.

        Crea una instancia de FlaskLoginUser a partir de un diccionario de usuario
        y utiliza `flask_login.login_user` para establecer la sesión.

        Args:
            dicc_usuario (dict): Diccionario con los datos del usuario a loguear.
        """
        user = FlaskLoginUser(dicc_usuario)
        login_user(user)
        print(f"Usuario {current_user.nombre} ha iniciado sesión")

    def logout_usuario(self):
        """
        Cierra la sesión del usuario actual.

        Utiliza `flask_login.logout_user` para finalizar la sesión del usuario.
        """
        logout_user()
        print("Usuario ha cerrado sesión")
        print(f"Usuario actual {current_user}")

    def admin_only(self, f):
        """
        Decorador para restringir el acceso a rutas solo para administradores.

        Un "administrador" se define como un usuario cuyo ID está en `__admin_list`.
        Si un usuario no autenticado o no administrador intenta acceder a la ruta,
        se aborta con un error 403 (Forbidden).

        Args:
            f (function): La función de vista de Flask a decorar.

        Returns:
            function: La función de vista decorada.
        """
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if current_user.is_authenticated and current_user.id not in self.__admin_list:
                return abort(403)
            return f(*args, **kwargs)
        return decorated_function
    
    def se_requiere_login(self, func):
        """
        Decorador para asegurar que una ruta solo sea accesible para usuarios autenticados.

        Este es un wrapper directo del decorador `login_required` de Flask-Login.

        Args:
            func (function): La función de vista de Flask a decorar.

        Returns:
            function: La función de vista decorada.
        """
        return login_required(func)
    
    def es_admin(self):
        """
        Verifica si el usuario actualmente autenticado es un administrador.

        Un administrador es un usuario autenticado cuyo ID se encuentra en la lista `__admin_list`.

        Returns:
            bool: True si el usuario es un administrador, False en caso contrario.
        """
        if current_user.is_authenticated and current_user.id in self.__admin_list:
            return True
        else:
            return False
        
