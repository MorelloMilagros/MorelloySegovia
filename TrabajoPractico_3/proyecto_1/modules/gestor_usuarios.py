from modules.repositorio_abstracto import RepositorioAbstracto
from modules.dominio import Usuario
from werkzeug.security import generate_password_hash, check_password_hash

class GestorDeUsuarios:
    def __init__(self, repo: RepositorioAbstracto):
        self.__repo = repo
    
    def registrar_nuevo_usuario(self,nombre,apellido,username,email,password,claustro):
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
        usuario = self.__repo.obtener_registro_por_filtro("email", email)
        if not usuario:
            raise ValueError("El usuario no está registrado")
        elif not check_password_hash(usuario.password, password):
            raise ValueError("Contraseña incorrecta")
        return usuario.to_dict()
    
    def cargar_usuario(self, id_usuario):
        usuario=self.__repo.obtener_registro_por_filtro("id", id_usuario)
        if not usuario:
            return None
        return usuario.to_dict()
    
    def modificar_rol(self, id_usuario, nuevo_rol):
        usuario= self.__repo.obtener_registro_por_filtro("id", id_usuario)
        if not usuario:
            raise ValueError("El usuario no existe")
        usuario.rol= nuevo_rol
        self.__repo.modificar_registro(usuario)
    
    