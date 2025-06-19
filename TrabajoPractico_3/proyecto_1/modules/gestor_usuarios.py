from modules.repositorio_abstracto import RepositorioAbstracto
from modules.dominio import Usuario
from werkzeug.security import generate_password_hash, check_password_hash

class GestorDeUsuarios:
    """
    Clase que encapsula la lógica de negocio para la gestión de usuarios.

    Maneja operaciones como el registro de nuevos usuarios, la autenticación
    de credenciales y la modificación de roles de usuario.

    Atributos:
        __repo (RepositorioAbstracto): Una instancia del repositorio de usuarios
                                      para interactuar con la persistencia.
    """
    def __init__(self, repo: RepositorioAbstracto):
        """
        Inicializa el GestorDeUsuarios.

        Args:
            repo (RepositorioAbstracto): La implementación del repositorio de usuarios a utilizar.
        """
        self.__repo = repo
    
    def registrar_nuevo_usuario(self,nombre,apellido,username,email,password,claustro):
        """
        Registra un nuevo usuario en el sistema.

        Antes de registrar, verifica que el email y el nombre de usuario no existan.
        La contraseña se encripta antes de ser almacenada.

        Args:
            nombre (str): Nombre del usuario.
            apellido (str): Apellido del usuario.
            username (str): Nombre de usuario único.
            email (str): Email único del usuario.
            password (str): Contraseña en texto plano.
            claustro (str): Claustro del usuario ("estudiante", "docente", "pays").

        Raises:
            ValueError: Si el email o el nombre de usuario ya están registrados.
        """
        if self.__repo.obtener_registro_por_filtro("email", email):
            raise ValueError("El usuario ya está registrado, por favor inicie sesion.")
        if self.__repo.obtener_registro_por_filtro("username", username):
            raise ValueError("El nombre de usuario ya está registrado.")
        pass_encriptada=generate_password_hash(password= password,
                                               method= 'pbkdf2:sha256',
                                               salt_length=8)
        usuario=Usuario(None,nombre,apellido,username, email, pass_encriptada, rol="usuario", p_departamento="sin departamento",p_claustro=claustro)
        self.__repo.guardar_registro(usuario)

    def autenticar_usuario(self, email, password):
        """
        Autentica a un usuario verificando sus credenciales.

        Busca al usuario por email y compara la contraseña proporcionada
        con la contraseña hasheada almacenada.

        Args:
            email (str): El email del usuario.
            password (str): La contraseña en texto plano proporcionada por el usuario.

        Returns:
            dict: Un diccionario con los datos del usuario si la autenticación es exitosa.

        Raises:
            ValueError: Si el usuario no está registrado o la contraseña es incorrecta.
        """
        usuario = self.__repo.obtener_registro_por_filtro("email", email)
        if not usuario:
            raise ValueError("El usuario no está registrado")
        elif not check_password_hash(usuario.password, password):
            raise ValueError("Contraseña incorrecta")
        return usuario.to_dict()
    
    def cargar_usuario(self, id_usuario):
        """
        Carga los datos de un usuario por su ID.

        Este método es utilizado principalmente por Flask-Login para recargar
        el objeto de usuario desde la sesión.

        Args:
            id_usuario (int): El ID del usuario a cargar.

        Returns:
            dict or None: Un diccionario con los datos del usuario si se encuentra,
                          o None si no existe.
        """
        usuario=self.__repo.obtener_registro_por_filtro("id", id_usuario)
        if not usuario:
            return None
        return usuario.to_dict()
    
    def modificar_rol(self, id_usuario, nuevo_rol):
        """
        Modifica el rol de un usuario existente.

        Args:
            id_usuario (int): El ID del usuario cuyo rol se va a modificar.
            nuevo_rol (str): El nuevo rol a asignar al usuario.

        Raises:
            ValueError: Si el usuario con el ID especificado no existe.
        """
        usuario= self.__repo.obtener_registro_por_filtro("id", id_usuario)
        if not usuario:
            raise ValueError("El usuario no existe")
        usuario.rol= nuevo_rol
        self.__repo.modificar_registro(usuario)
    
    