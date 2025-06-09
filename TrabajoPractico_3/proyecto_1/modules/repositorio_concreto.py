from modules.repositorio_abstracto import RepositorioAbstracto
from modules.modelos import ModeloReclamo, ModeloUsuario, Adherencia
from modules.dominio import Reclamo, Usuario

class RepositorioReclamosSQLAlchemy(RepositorioAbstracto):
    def __init__(self, session):
        self.__session= session
        ModeloReclamo.metadata.create_all(self.__session.bind)

    def guardar_registro(self, reclamo):
        if not isinstance(reclamo, Reclamo):
            raise ValueError("El parametro no es una instancia de la clase reclamo")
        modelo_reclamo= self.__map_entidad_a_modelo(reclamo)
        self.__session.add(modelo_reclamo)
        self.__session.commit()

    def obtener_todos_los_registros(self):
        modelo_reclamos= self.__session.query(ModeloReclamo).all()
        return [self.__map_modelo_a_entidad(reclamo) for reclamo in modelo_reclamos]

    def modificar_registro(self, reclamo_modificado):
        if not isinstance(reclamo_modificado, Reclamo):
            raise ValueError("El parametro no es una instancia de la clase reclamo")
        registro= self.__session.query(ModeloReclamo).filter_by(id=reclamo_modificado.id).first()
        if registro:
            registro.descripcion= reclamo_modificado.descripcion
            registro.estado= reclamo_modificado.estado
            self.__session.commit()
        else:
            raise ValueError("El reclamo no existe en la base de datos")
    

    def obtener_registro_por_filtro(self, filtro, valor):
        modelo_reclamo=self.__session.query(ModeloReclamo).filter_by(**{filtro: valor}).first()
        return self.__map_modelo_a_entidad(modelo_reclamo) if modelo_reclamo else None
    
    def eliminar_registro(self, id):
        registro= self.__session.query(ModeloReclamo).filter_by(id=id).first()
        self.__session.delete(registro)
        self.__session.commit()

    def __map_entidad_a_modelo(self, entidad: Reclamo):
        return ModeloReclamo(
            id= entidad.id,
            descripcion=entidad.descripcion,
            estado=entidad.estado,
            id_usuario=entidad.id_usuario
            )
    
    def __map_modelo_a_entidad(self, modelo: ModeloReclamo):
        return Reclamo(
            modelo.id,
            modelo.descripcion,
            modelo.estado,
            modelo.id_usuario
        )
    
    def adherir_usuario_a_reclamo(self,id_usuario, id_reclamo):
        #Verificamos si ya esta adherido
        existe=self.__session.query(Adherencia).filter_by(id_usuario=id_usuario, id_reclamo=id_reclamo).first()

        if existe:
            raise ValueError("El usuario ya está adherido a este reclamo")
        
        adherencia=Adherencia(id_usuario=id_usuario, id_reclamo=id_reclamo)
        self.__session.add(adherencia)
        self.__session.commit()

    def contar_adherentes(self, id_reclamo):
            return self.__session.query(Adherencia).filter_by(id_reclamo=id_reclamo).count()
    
    def obtener_adherentes(self, id_reclamo):
        adherencias= self.__session.query(Adherencia).filter_by(id_reclamo=id_reclamo).all()
        return [a.id_usuario for a in adherencias]
    
class RepositorioUsuariosSQLAlchemy(RepositorioAbstracto):
    def __init__(self, session):
        self.__session = session
        ModeloUsuario.metadata.create_all(self.__session.bind)

    def guardar_registro(self, usuario):
        if not isinstance(usuario, Usuario):
            raise ValueError("El parámetro no es una instancia de la clase Usuario")
        modelo_usuario = self.__map_entidad_a_modelo(usuario)
        self.__session.add(modelo_usuario)
        try: 
            self.__session.commit()
        except Exception as e:
            self.__session.rollback()
            raise ValueError(f"Error al guardar usuario: {str(e)}")

    def obtener_todos_los_registros(self):
        modelo_usuarios = self.__session.query(ModeloUsuario).all()
        return [self.__map_modelo_a_entidad(usuario) for usuario in modelo_usuarios]   
    
    def modificar_registro(self, usuario_modificado):
        if not isinstance(usuario_modificado, Usuario):
            raise ValueError("El parámetro no es una instancia de la clase Usuario")
        register = self.__session.query(ModeloUsuario).filter_by(id=usuario_modificado.id).first()
        if register:
            register.nombre = usuario_modificado.nombre
            register.email = usuario_modificado.email
            register.password = usuario_modificado.password
            register.rol= usuario_modificado.rol
            self.__session.commit()
        else:
            raise ValueError("El usuario no existe en la base de datis")

    def obtener_registro_por_filtro(self, filtro, valor):
        modelo_usuario = self.__session.query(ModeloUsuario).filter_by(**{filtro:valor}).first()
        return self.__map_modelo_a_entidad(modelo_usuario) if modelo_usuario else None
    
    def eliminar_registro(self, id):
        register = self.__session.query(ModeloUsuario).filter_by(id=id).first()
        if register:
            self.__session.delete(register)
            self.__session.commit()
        else:
            raise ValueError("El usuario no existe en la base de datos")
    def __map_entidad_a_modelo(self, entidad: Usuario):
        return ModeloUsuario(
            id= entidad.id,
            nombre=entidad.nombre,
            email=entidad.email,
            password=entidad.password,
            rol=entidad.rol,
            departamento=entidad.departamento
        )
    
    def __map_modelo_a_entidad(self, modelo: ModeloUsuario):
        return Usuario(
            modelo.id,
            modelo.nombre,
            modelo.email,
            modelo.password,
            modelo.rol,
            modelo.departamento
        )