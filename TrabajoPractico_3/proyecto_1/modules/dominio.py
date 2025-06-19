from datetime import datetime

class Reclamo:
    """
    Representa un reclamo dentro del sistema de la Facultad de Ingeniería de la UNER.

    Esta clase encapsula la información y el comportamiento de un reclamo,
    incluyendo su descripción, estado actual, departamento al que pertenece,
    y las fechas de creación y posible resolución.

    Atributos:
        id (int, opcional): Identificador único del reclamo. Se asigna None para nuevos reclamos.
        descripcion (str): Contenido textual del problema reportado.
        estado (str): Estado actual del reclamo ("pendiente", "en proceso", "resuelto", "inválido").
        id_usuario (int): ID del usuario que originó el reclamo.
        departamento (str): Departamento al que se asigna el reclamo.
        fecha_creacion (datetime, opcional): Fecha y hora de creación del reclamo.
                                             Por defecto, se usa la fecha y hora actuales si no se provee.
        foto (str, opcional): Ruta o nombre del archivo de la foto adjunta al reclamo.
        fecha_resolucion (datetime, opcional): Fecha estimada o real de resolución del reclamo.
    """
    def __init__(self, p_id, p_descripcion, p_estado, pd_id_usuario, p_departamento="sin departamento", p_fecha_creacion=None, p_foto=None, p_fecha_resolucion=None):
        self.id= p_id
        self.descripcion=p_descripcion
        self.estado =p_estado
        self.id_usuario= pd_id_usuario
        self.departamento= p_departamento
        
        # Si no se proporciona una fecha de creación, usamos la fecha y hora actuales.
        self.fecha_creacion = p_fecha_creacion or datetime.now()
        # ----------------------------------------
        
        self.foto=p_foto
        self.fecha_resolucion=p_fecha_resolucion
    
    @property
    def id(self):
        """Obtiene el ID del reclamo."""
        return self.__id
    
    @property
    def descripcion(self):
        """Obtiene la descripción del reclamo."""
        return self.__descripcion
    
    @property
    def estado(self):
        """Obtiene el estado actual del reclamo."""
        return self.__estado
    
    @property 
    def id_usuario(self):
        """Obtiene el ID del usuario creador del reclamo."""
        return self.__id_usuario
    
    @property
    def departamento(self):
        """Obtiene el departamento al que pertenece el reclamo."""
        return self.__departamento
    
    @property
    def fecha_creacion(self):
        """Obtiene la fecha y hora de creación del reclamo."""
        return self.__fecha_creacion
    
    @property
    def foto(self):
        """Obtiene la ruta o nombre del archivo de la foto adjunta."""
        return self.__foto
    
    @property
    def fecha_resolucion(self):
        """Obtiene la fecha estimada o real de resolución del reclamo."""
        return self.__fecha_resolucion
    
    @id.setter
    def id(self, p_id):
        """
        Establece el ID del reclamo.

        Args:
            p_id (int): El ID a establecer. Debe ser un entero.
        Raises:
            ValueError: Si el ID no es un número entero.
        """
        if p_id is not None and not isinstance(p_id, int):
            raise ValueError("El id debe ser un número entero")
        self.__id=p_id

    @descripcion.setter
    def descripcion(self, p_descripcion):
        """
        Establece la descripción del reclamo.

        Args:
            p_descripcion (str): La descripción a establecer. No puede estar vacía.
        Raises:
            ValueError: Si la descripción no es una cadena o está vacía.
        """
        if not isinstance(p_descripcion, str) or p_descripcion.strip() == "":
            raise ValueError("La descripcion no puede estar vacía")
        self.__descripcion= p_descripcion.strip()

    @estado.setter
    def estado(self, p_estado):
        """
        Establece el estado del reclamo.

        Args:
            p_estado (str): El estado a establecer. Debe ser uno de "pendiente",
                            "resuelto", "en proceso", "inválido".
        Raises:
            ValueError: Si el estado no es uno de los valores permitidos.
        """
        if p_estado not in ["pendiente", "resuelto", "en proceso","inválido"]:
            raise ValueError("El estado debe ser 'pendiente', 'resuelto', 'en proceso' o 'invalido'")
        self.__estado=p_estado

    @id_usuario.setter
    def id_usuario(self, p_id_usuario):
        """
        Establece el ID del usuario creador del reclamo.

        Args:
            p_id_usuario (int): El ID de usuario a establecer. Debe ser un entero.
        Raises:
            ValueError: Si el ID de usuario no es un número entero.
        """
        if  p_id_usuario is not None and not isinstance(p_id_usuario, int):
            raise ValueError("El ID de usuario debe ser un número entero")
        self.__id_usuario=p_id_usuario

    @departamento.setter
    def departamento(self, p_departamento):
        """
        Establece el departamento al que pertenece el reclamo.

        Args:
            p_departamento (str): El departamento a establecer. No puede estar vacío.
        Raises:
            ValueError: Si el departamento no es una cadena o está vacía.
        """
        # Eliminamos el print de debug para limpiar la consola
        if not isinstance(p_departamento, str) or p_departamento.strip()== "":
            raise ValueError("El departamento no puede estar vacío")
        self.__departamento=p_departamento

    @fecha_creacion.setter
    def fecha_creacion(self, p_fecha_creacion):
        """
        Establece la fecha y hora de creación del reclamo.

        Args:
            p_fecha_creacion (datetime): La fecha de creación a establecer.
        """
        self.__fecha_creacion= p_fecha_creacion

    @foto.setter
    def foto(self, p_foto):
        """
        Establece la ruta o nombre del archivo de la foto adjunta.

        Args:
            p_foto (str, opcional): La ruta de la foto a establecer.
        """
        self.__foto=p_foto

    @fecha_resolucion.setter
    def fecha_resolucion(self, p_fecha_resolucion):
        """
        Establece la fecha estimada o real de resolución del reclamo.

        Args:
            p_fecha_resolucion (datetime, opcional): La fecha de resolución a establecer.
        """
        self.__fecha_resolucion= p_fecha_resolucion

    def calcular_tiempo_resolucion(self):
        """
        Calcula el tiempo de resolución de un reclamo en días.

        El cálculo se realiza solo si tanto `fecha_creacion` como `fecha_resolucion`
        están presentes.

        Returns:
            int or None: El número de días transcurridos entre la creación y la resolución,
                         o None si alguna de las fechas no está definida.
        """
        if self.fecha_resolucion and self.fecha_creacion:
            return (self.fecha_resolucion - self.fecha_creacion).days
        return None

    def to_dict(self):
        """
        Convierte el objeto Reclamo a un diccionario.

        Útil para serialización, paso de datos a plantillas HTML o APIs.

        Returns:
            dict: Un diccionario con los atributos del reclamo.
        """
        return {
            "id":self.id,
            "descripcion":self.descripcion,
            "estado": self.estado,
            "id_usuario": self.id_usuario,
            "departamento": self.departamento,
            "fecha_creacion": self.fecha_creacion, # Devolvemos el objeto datetime, no un string
            "fecha_resolucion":self.fecha_resolucion,
            "foto":self.foto
        }
    
    def __str__(self):
        """
        Retorna una representación en cadena del objeto Reclamo.

        Útil para depuración y visualización rápida.
        """
        return  f"Reclamo {self.id}: {self.descripcion} (Estado: {self.estado}) "


class Usuario:
    """
    Representa un usuario del sistema de reclamos.

    Esta clase encapsula la información personal de un usuario, sus credenciales,
    su rol dentro del sistema (ej. "usuario", "jefe", "secretario") y su claustro.
    También implementa métodos requeridos por Flask-Login para la gestión de sesiones.

    Atributos:
        id (int, opcional): Identificador único del usuario. Se asigna None para nuevos usuarios.
        nombre (str): Nombre del usuario.
        apellido (str): Apellido del usuario.
        username (str): Nombre de usuario único para login.
        email (str): Dirección de correo electrónico única del usuario.
        password (str): Contraseña hash del usuario.
        rol (str): Rol del usuario ("usuario", "jefe", "secretario", "tecnico").
        departamento (str): Departamento asociado al usuario (si aplica, ej. para jefes).
        claustro (str): Claustro al que pertenece el usuario ("estudiante", "docente", "pays").
    """
    def __init__(self, p_id, p_nombre,p_apellido,p_username, p_email, p_password, rol, p_departamento, p_claustro):
        """
        Constructor de la clase Usuario.

        Args:
            p_id (int, opcional): El ID del usuario.
            p_nombre (str): El nombre del usuario.
            p_apellido (str): El apellido del usuario.
            p_username (str): El nombre de usuario único.
            p_email (str): El email único del usuario.
            p_password (str): La contraseña (ya hasheada o a hashear).
            rol (str): El rol del usuario.
            p_departamento (str, opcional): El departamento asociado (por defecto "sin departamento").
            p_claustro (str): El claustro al que pertenece el usuario.
        """
        self.id = p_id
        self.nombre = p_nombre
        self.apellido= p_apellido
        self.username=p_username
        self.email = p_email
        self.password = p_password
        self.rol=rol
        self.departamento= p_departamento or "sin departamento"
        self.claustro=p_claustro
        
    def es_jefe(self):
        """
        Verifica si el usuario tiene el rol de "jefe".

        Returns:
            bool: True si el rol es "jefe", False en caso contrario.
        """
        return self.rol == 'jefe'

    def es_secretario(self):
        """
        Verifica si el usuario tiene el rol de "secretario".

        Returns:
            bool: True si el rol es "secretario", False en caso contrario.
        """
        return self.rol == 'secretario'

    @property
    def is_active(self):
        """
        Propiedad requerida por Flask-Login.

        Indica si el usuario está activo (ej. no deshabilitado).
        Para este sistema, todos los usuarios son considerados activos.
        """
        return True

    @property
    def is_authenticated(self):
        """
        Propiedad requerida por Flask-Login.

        Indica si el usuario ha sido autenticado exitosamente.
        """
        return True

    def get_id(self):
        """
        Método requerido por Flask-Login para obtener el ID de usuario.

        El ID devuelto debe ser una cadena (str) compatible con Flask-Login.

        Returns:
            str: El ID del usuario como cadena.
        """
        return str(self.id)

    @property
    def id(self):
        """Obtiene el ID del usuario."""
        return self.__id
    
    @property
    def nombre(self):
        """Obtiene el nombre del usuario."""
        return self.__nombre
    
    @property
    def apellido(self):
        """Obtiene el apellido del usuario."""
        return self.__apellido
    
    @property 
    def username(self):
        """Obtiene el nombre de usuario."""
        return self.__username
    
    @property
    def email(self):
        """Obtiene el correo electrónico del usuario."""
        return self.__email
    
    @property
    def password(self):
        """Obtiene la contraseña hash del usuario."""
        return self.__password
    
    @property 
    def rol(self):
        """Obtiene el rol del usuario."""
        return self.__rol
    
    @property
    def departamento(self):
        """Obtiene el departamento asociado al usuario."""
        return self.__departamento
    
    @property
    def claustro(self):
        """Obtiene el claustro al que pertenece el usuario."""
        return self.__claustro
    
    @id.setter
    def id(self, p_id):
        """
        Establece el ID del usuario.

        Args:
            p_id (int, opcional): El ID a establecer. Puede ser None o un entero.
        Raises:
            ValueError: Si el ID no es None y no es un entero.
        """
        if p_id != None:
            if not isinstance(p_id, int):
                raise ValueError("El id del usuario debe ser un número entero")
            self.__id = p_id
        else:
            self.__id = None
    
    @nombre.setter
    def nombre(self, p_nombre:str):
        """
        Establece el nombre del usuario.

        Args:
            p_nombre (str): El nombre a establecer. Debe ser una cadena no vacía.
        Raises:
            ValueError: Si el nombre no es una cadena o está vacía.
        """
        if not isinstance(p_nombre, str) or p_nombre.strip() == "":
            raise ValueError("El nombre del usuario debe ser un string y no debe estar vacío")
        self.__nombre = p_nombre.strip()

    @apellido.setter
    def apellido(self, p_apellido:str):
        """
        Establece el apellido del usuario.

        Args:
            p_apellido (str): El apellido a establecer. Debe ser una cadena no vacía.
        Raises:
            ValueError: Si el apellido no es una cadena o está vacía.
        """
        if not isinstance(p_apellido, str) or p_apellido.strip()=="":
            raise ValueError("El apellido del usuario debe ser un string y no debe estar vacío")
        self.__apellido= p_apellido.strip()

    @username.setter
    def username(self, p_username: str):
        """
        Establece el nombre de usuario.

        Args:
            p_username (str): El nombre de usuario a establecer. Debe ser una cadena no vacía.
        Raises:
            ValueError: Si el nombre de usuario no es una cadena o está vacía.
        """
        if not isinstance(p_username, str) or p_username.strip() == "":
            raise ValueError("El usuario debe ser un string y no debe estar vacío")
        self.__username = p_username.strip()
        
    @email.setter # This line should have the correct indentation
    def email(self, p_email: str):
        """ # This docstring must be immediately inside the def, and correctly indented
        Establece el correo electrónico del usuario.

        Args:
            p_email (str): El email a establecer. Debe ser una cadena no vacía.
        Raises:
            ValueError: Si el email no es una cadena o está vacía.
        """
        if not isinstance(p_email, str) or p_email.strip() == "":
            raise ValueError("El email de usuario debe ser un string y no debe estar vacío")
        self.__email = p_email.strip()
        
    @password.setter # This line should have the correct indentation
    def password(self, password: str):
        """ # This docstring must be immediately inside the def, and correctly indented
        Establece la contraseña hash del usuario.

        Args:
            password (str): La contraseña hash a establecer.
        """
        self.__password = password

    @rol.setter # This line should have the correct indentation
    def rol(self, rol: str):
        """ # This docstring must be immediately inside the def, and correctly indented
        Establece el rol del usuario.

        Args:
            rol (str): El rol a establecer.
        """
        self.__rol = rol
    
    @departamento.setter
    def departamento(self, p_departamento):
        """
        Establece el departamento del usuario.

        Args:
            p_departamento (str): El departamento a establecer. Debe ser una cadena.
        Raises:
            ValueError: Si el departamento no es una cadena.
        """
        if not isinstance(p_departamento, str):
            raise ValueError("El departamento debe ser una cadena")
        self.__departamento= p_departamento

    @claustro.setter
    def claustro(self, p_claustro):
        """
        Establece el claustro del usuario.

        Args:
            p_claustro (str): El claustro a establecer. Debe ser "estudiante", "docente" o "pays".
        Raises:
            ValueError: Si el claustro es inválido.
        """
        if p_claustro not in ["estudiante", "docente", "pays"]:
            raise ValueError("Claustro Inválido")
        self.__claustro=p_claustro
        
    def to_dict(self):
        """
        Convierte el objeto Usuario a un diccionario.

        Útil para serialización o para pasar datos a otras capas de la aplicación.

        Returns:
            dict: Un diccionario con los atributos del usuario.
        """
        return {
            "id": self.id,
            "nombre": self.nombre,
            "apelldio":self.apellido,
            "username":self.username,
            "email": self.email,
            "password": self.password,
            "rol": self.rol,
            "departamento":self.departamento,
            "claustro":self.claustro
        }
