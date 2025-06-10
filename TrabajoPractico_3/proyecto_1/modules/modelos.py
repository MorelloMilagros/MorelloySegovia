from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Table
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
Base=declarative_base()

class ModeloReclamo(Base):
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
        """"""
        if self.fecha_resolucion:
            return (self.fecha_resolucion- self.fecha_creacion).days
        else:
            return None

class ModeloUsuario(Base):
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
        return self.rol=="jefe"
    
    def es_secretario(self):
        return self.rol == "secretario"
       
    def es_tecnico(self):
        return self.rol == "tecnico"
    
class Adherencia(Base):
    __tablename__= 'adherencias'   
    id=Column(Integer, primary_key=True)
    id_usuario=Column(Integer, ForeignKey("usuarios.id"))
    id_reclamo=Column(Integer, ForeignKey("reclamos.id"))

    


