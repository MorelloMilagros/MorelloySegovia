from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base=declarative_base()

class ModeloReclamo(Base):
    __tablename__= 'reclamos'
    id= Column(Integer, primary_key=True)
    descripcion= Column(String(1000), nullable=False)
    estado= Column(String(50), default="Pendiente") #El estado. Puede ser Pendiente, o Resuelto
    id_usuario= Column(Integer, ForeignKey('usuarios.id')) #Reclamo ligado a usuario

class ModeloUsuario(Base):
    __tablename__= 'usuarios'
    id= Column(Integer, primary_key=True)
    nombre=Column(String(1000), nullable=False, unique=True)
    email= Column(String(1000), nullable=False, unique=True)
    password= Column(String(1000), nullable=False)
    rol=Column(String, default="usuario")
    def es_jefe(self):
        return self.rol=="jefe"
    
    def es_secretario(self):
        return self.rol == "secretario"
       


