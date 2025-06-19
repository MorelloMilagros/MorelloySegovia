from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Table
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
Base=declarative_base()

class ModeloReclamo(Base):
    """
    Representa el modelo de la tabla 'reclamos' en la base de datos.

    Define la estructura de la tabla para almacenar la información de los reclamos,
    incluyendo sus atributos, tipos de datos y relaciones.

    Atributos de la tabla:
        id (Integer): Clave primaria, autoincremental.
        descripcion (String): Texto del reclamo. No puede ser nulo.
        estado (String): Estado del reclamo (ej. "pendiente", "resuelto"). Valor por defecto "pendiente".
        departamento (String): Departamento asignado al reclamo. No puede ser nulo.
        fecha_creacion (DateTime): Fecha y hora de creación. Valor por defecto la hora UTC actual.
        fecha_resolucion (DateTime): Fecha y hora de resolución. Puede ser nulo.
        id_usuario (Integer): Clave foránea que referencia el ID del usuario creador en la tabla 'usuarios'.
        foto (String): Ruta del archivo de la foto adjunta. Puede ser nulo.
    """
    __tablename__= 'reclamos'
    id= Column(Integer, primary_key=True)
    descripcion= Column(String(1000), nullable=False)
    estado= Column(String(50), default="pendiente") #El estado. Puede ser Pendiente, o Resuelto
    departamento= Column(String(100), nullable=False)
    fecha_creacion= Column(DateTime, default=datetime.utcnow)
    fecha_resolucion= Column(DateTime, nullable=True)    
    id_usuario= Column(Integer, ForeignKey('usuarios.id')) #Reclamo ligado a usuario
    foto = Column(String(255), nullable=True)


    def calcular_tiempo_resolucion(self):
        """
        Calcula el tiempo de resolución en días para este modelo de reclamo.

        Si la `fecha_resolucion` está definida, calcula la diferencia en días
        desde la `fecha_creacion`.

        Returns:
            int or None: El número de días si el reclamo está resuelto, de lo contrario, None.
        """
        """"""
        if self.fecha_resolucion:
            return (self.fecha_resolucion- self.fecha_creacion).days
        else:
            return None

class ModeloUsuario(Base):
    """
    Representa el modelo de la tabla 'usuarios' en la base de datos.

    Define la estructura de la tabla para almacenar la información de los usuarios,
    incluyendo sus datos personales, credenciales y rol.

    Atributos de la tabla:
        id (Integer): Clave primaria, autoincremental.
        nombre (String): Nombre del usuario. No puede ser nulo.
        apellido (String): Apellido del usuario. No puede ser nulo.
        username (String): Nombre de usuario. Único y no puede ser nulo.
        email (String): Correo electrónico. Único y no puede ser nulo.
        password (String): Contraseña hasheada. No puede ser nulo.
        rol (String): Rol del usuario (ej. "usuario", "jefe", "secretario", "tecnico"). Valor por defecto "usuario".
        claustro (String): Claustro al que pertenece (ej. "estudiante", "docente", "pays"). No puede ser nulo.
        departamento (String): Departamento asociado al usuario (para roles de personal). Valor por defecto "sin_departamento".
    """
    __tablename__= 'usuarios'
    id= Column(Integer, primary_key=True)
    nombre=Column(String(1000), nullable=False, unique=False)
    apellido=Column(String(1000), nullable=False, unique= False)
    username=Column(String(100), nullable=False, unique=True)
    email= Column(String(1000), nullable=False, unique=True)
    password= Column(String(1000), nullable=False)
    rol=Column(String, default="usuario")
    claustro=Column(String(100), nullable=False)
    departamento = Column(String(100), default="sin_departamento")

    #Roles
    def es_jefe(self):
        """
        Verifica si el rol del modelo de usuario es "jefe".
        """
        return self.rol=="jefe"
    
    def es_secretario(self):
        """
        Verifica si el rol del modelo de usuario es "secretario".
        """
        return self.rol == "secretario"
       
    def es_tecnico(self):
        """
        Verifica si el rol del modelo de usuario es "tecnico".
        """
        return self.rol == "tecnico"
    
class Adherencia(Base):
    """
    Representa el modelo de la tabla 'adherencias' en la base de datos.

    Esta tabla intermedia (tabla de unión) se utiliza para modelar la relación
    muchos-a-muchos entre usuarios y reclamos, permitiendo que múltiples usuarios
    se adhieran a un mismo reclamo.

    Atributos de la tabla:
        id (Integer): Clave primaria, autoincremental.
        id_usuario (Integer): Clave foránea que referencia el ID del usuario adherido.
        id_reclamo (Integer): Clave foránea que referencia el ID del reclamo al que se adhiere.
    """
    __tablename__= 'adherencias'   
    id=Column(Integer, primary_key=True)
    id_usuario=Column(Integer, ForeignKey("usuarios.id"))
    id_reclamo=Column(Integer, ForeignKey("reclamos.id"))

    


