from modules.repositorio_abstracto import RepositorioAbstracto
from modules.modelos import ModeloReclamo, ModeloUsuario, Adherencia
from modules.dominio import Reclamo, Usuario
from datetime import datetime
from sqlalchemy import func 


class RepositorioReclamosSQLAlchemy(RepositorioAbstracto):
    """
    Implementación concreta del RepositorioAbstracto para la entidad Reclamo,
    utilizando SQLAlchemy para la persistencia en una base de datos relacional.

    Esta clase maneja las operaciones de guardar, obtener, modificar y eliminar
    reclamos, traduciendo entre objetos de dominio (Reclamo) y modelos de
    base de datos (ModeloReclamo).

    Atributos:
        __session (Session): Una instancia de la sesión de SQLAlchemy para
                             interactuar con la base de datos.
    """
    def __init__(self, session):
        """
        Inicializa el repositorio de reclamos con una sesión de SQLAlchemy.

        Args:
            session (sqlalchemy.orm.session.Session): La sesión de base de datos de SQLAlchemy.
        """
        self.__session= session
        ModeloReclamo.metadata.create_all(self.__session.bind)

    def guardar_registro(self, reclamo):
        """
        Guarda un nuevo objeto Reclamo en la base de datos.

        Convierte el objeto de dominio `Reclamo` a su modelo de SQLAlchemy (`ModeloReclamo`)
        y lo añade a la sesión para su persistencia.

        Args:
            reclamo (Reclamo): El objeto Reclamo a guardar.

        Raises:
            ValueError: Si el objeto proporcionado no es una instancia de Reclamo.
            Exception: Cualquier error que ocurra durante la transacción de la base de datos.
        """
        if not isinstance(reclamo, Reclamo):
            raise ValueError("El parametro no es una instancia de la clase reclamo")
        modelo_reclamo= self.__map_entidad_a_modelo(reclamo)
        self.__session.add(modelo_reclamo)
        self.__session.commit()

    def obtener_todos_los_registros(self):
        """
        Obtiene todos los registros de reclamos de la base de datos.

        Retorna una lista de objetos de dominio `Reclamo`.

        Returns:
            list[Reclamo]: Una lista de todos los reclamos.
        """
        modelo_reclamos= self.__session.query(ModeloReclamo).all()
        return [self.__map_modelo_a_entidad(reclamo) for reclamo in modelo_reclamos]

    def modificar_registro(self, reclamo_modificado):
        """
        Modifica un reclamo existente en la base de datos.

        Busca el reclamo por su ID y actualiza sus atributos con los valores
        del objeto `reclamo_modificado`.

        Args:
            reclamo_modificado (Reclamo): El objeto Reclamo con los datos actualizados.

        Raises:
            ValueError: Si el objeto proporcionado no es una instancia de Reclamo
                        o si el reclamo no existe en la base de datos.
            Exception: Cualquier error que ocurra durante la transacción de la base de datos.
        """
        if not isinstance(reclamo_modificado, Reclamo):
            raise ValueError("El parametro no es una instancia de la clase reclamo")
        registro= self.__session.query(ModeloReclamo).filter_by(id=reclamo_modificado.id).first()
        if registro:
            registro.descripcion= reclamo_modificado.descripcion
            registro.estado= reclamo_modificado.estado
            registro.departamento=reclamo_modificado.departamento
            registro.fecha_resolucion= reclamo_modificado.fecha_resolucion
            registro.foto=reclamo_modificado.foto
            self.__session.commit()
        else:
            raise ValueError("El reclamo no existe en la base de datos")
    

    def obtener_registro_por_filtro(self, filtro, valor):
        """
        Obtiene un único reclamo de la base de datos por un filtro específico.

        Args:
            filtro (str): El nombre del atributo del modelo (ej. "id", "departamento")
                          por el cual filtrar.
            valor (any): El valor a buscar.

        Returns:
            Reclamo or None: El objeto Reclamo si se encuentra un match, de lo contrario, None.
        """
        modelo_reclamo=self.__session.query(ModeloReclamo).filter_by(**{filtro: valor}).first()
        return self.__map_modelo_a_entidad(modelo_reclamo) if modelo_reclamo else None

    def obtener_registros_por_filtros(self, **filtros):
        """
        Obtiene una lista de reclamos que coinciden con múltiples criterios de filtro.

        Permite filtrar por cualquier atributo del ModeloReclamo. Para el filtro
        por 'departamento', la comparación se realiza de forma insensible a mayúsculas/minúsculas.

        Args:
            **filtros: Argumentos de palabra clave donde la clave es el nombre del atributo
                       y el valor es el criterio de búsqueda (ej. `departamento="Soporte técnico"`).

        Returns:
            list[Reclamo]: Una lista de objetos Reclamo que satisfacen todos los filtros.
        """
        query = self.__session.query(ModeloReclamo)
        for clave, valor in filtros.items():
            if clave == 'departamento':
                # El especialista sabe cómo manejar este caso particular
                query = query.filter(func.lower(ModeloReclamo.departamento) == valor.lower())
            else:
                query = query.filter(getattr(ModeloReclamo, clave) == valor)

        modelo_reclamos = query.all()
        return [self.__map_modelo_a_entidad(reclamo) for reclamo in modelo_reclamos]
        
    def eliminar_registro(self, id):
        """
        Elimina un reclamo de la base de datos por su ID.

        Args:
            id (int): El ID del reclamo a eliminar.

        Raises:
            ValueError: Si el reclamo no existe en la base de datos.
            Exception: Cualquier error que ocurra durante la transacción de la base de datos.
        """
        registro= self.__session.query(ModeloReclamo).filter_by(id=id).first()
        self.__session.delete(registro)
        self.__session.commit()

    def __map_entidad_a_modelo(self, entidad: Reclamo):
        """
        Mapea un objeto de dominio Reclamo a un objeto ModeloReclamo (SQLAlchemy).

        Args:
            entidad (Reclamo): El objeto de dominio Reclamo.

        Returns:
            ModeloReclamo: La representación del reclamo lista para la base de datos.
        """
        return ModeloReclamo(
            id= entidad.id,
            descripcion=entidad.descripcion,
            estado=entidad.estado,
            id_usuario=entidad.id_usuario,
            departamento=entidad.departamento,
            fecha_creacion=entidad.fecha_creacion or datetime.utcnow(),
            foto=entidad.foto,
            fecha_resolucion=entidad.fecha_resolucion
            )
    
    def __map_modelo_a_entidad(self, modelo: ModeloReclamo):
        """
        Mapea un objeto ModeloReclamo (SQLAlchemy) a un objeto de dominio Reclamo.

        Args:
            modelo (ModeloReclamo): El modelo de reclamo de la base de datos.

        Returns:
            Reclamo: La representación del reclamo como objeto de dominio.
        """
        return Reclamo(
            modelo.id,
            modelo.descripcion,
            modelo.estado,
            int(modelo.id_usuario) if modelo.id_usuario is not None else None,
            modelo.departamento,
            modelo.fecha_creacion,
            modelo.foto,
            modelo.fecha_resolucion
        )
    
    def adherir_usuario_a_reclamo(self,id_usuario, id_reclamo):
        """
        Registra la adhesión de un usuario a un reclamo específico.

        Crea un nuevo registro en la tabla 'adherencias'.

        Args:
            id_usuario (int): El ID del usuario que se adhiere.
            id_reclamo (int): El ID del reclamo al que el usuario se adhiere.

        Raises:
            ValueError: Si el usuario ya está adherido a ese reclamo.
            Exception: Cualquier error que ocurra durante la transacción de la base de datos.
        """
        #Verificamos si ya esta adherido
        existe=self.__session.query(Adherencia).filter_by(id_usuario=id_usuario, id_reclamo=id_reclamo).first()

        if existe:
            raise ValueError("El usuario ya está adherido a este reclamo")
        
        adherencia=Adherencia(id_usuario=id_usuario, id_reclamo=id_reclamo)
        self.__session.add(adherencia)
        self.__session.commit()

    def contar_adherentes(self, id_reclamo):
        """
        Cuenta el número de usuarios adheridos a un reclamo dado.

        Args:
            id_reclamo (int): El ID del reclamo.

        Returns:
            int: La cantidad de adherentes para el reclamo.
        """
        return self.__session.query(Adherencia).filter_by(id_reclamo=id_reclamo).count()
    
    def obtener_adherentes(self, id_reclamo):
        """
        Obtiene la lista de IDs de usuarios adheridos a un reclamo.

        Args:
            id_reclamo (int): El ID del reclamo.

        Returns:
            list[int]: Una lista de IDs de usuario.
        """
        adherencias= self.__session.query(Adherencia).filter_by(id_reclamo=id_reclamo).all()
        return [a.id_usuario for a in adherencias]
    

class RepositorioUsuariosSQLAlchemy(RepositorioAbstracto):
    """
    Implementación concreta del RepositorioAbstracto para la entidad Usuario,
    utilizando SQLAlchemy para la persistencia.

    Maneja las operaciones CRUD para la entidad Usuario, traduciendo entre
    objetos de dominio (Usuario) y modelos de base de datos (ModeloUsuario).

    Atributos:
        __session (Session): Una instancia de la sesión de SQLAlchemy.
    """
    def __init__(self, session):
        """
        Inicializa el repositorio de usuarios con una sesión de SQLAlchemy.

        Args:
            session (sqlalchemy.orm.session.Session): La sesión de base de datos de SQLAlchemy.
        """
        self.__session = session
        ModeloUsuario.metadata.create_all(self.__session.bind)

    def guardar_registro(self, usuario):
        """
        Guarda un nuevo objeto Usuario en la base de datos.

        Convierte el objeto de dominio `Usuario` a su modelo de SQLAlchemy
        y lo añade a la sesión. Incluye manejo de excepciones para `commit`.

        Args:
            usuario (Usuario): El objeto Usuario a guardar.

        Raises:
            ValueError: Si el objeto proporcionado no es una instancia de Usuario,
                        o si hay un error al guardar (ej. clave única duplicada).
        """
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
        """
        Obtiene todos los registros de usuarios de la base de datos.

        Retorna una lista de objetos de dominio `Usuario`.

        Returns:
            list[Usuario]: Una lista de todos los usuarios.
        """
        modelo_usuarios = self.__session.query(ModeloUsuario).all()
        return [self.__map_modelo_a_entidad(usuario) for usuario in modelo_usuarios]   
    
    def modificar_registro(self, usuario_modificado):
        """
        Modifica un usuario existente en la base de datos.

        Busca el usuario por su ID y actualiza sus atributos.

        Args:
            usuario_modificado (Usuario): El objeto Usuario con los datos actualizados.

        Raises:
            ValueError: Si el objeto proporcionado no es una instancia de Usuario
                        o si el usuario no existe en la base de datos.
            Exception: Cualquier error que ocurra durante la transacción de la base de datos.
        """
        if not isinstance(usuario_modificado, Usuario):
            raise ValueError("El parámetro no es una instancia de la clase Usuario")
        register = self.__session.query(ModeloUsuario).filter_by(id=usuario_modificado.id).first()
        if register:
            register.nombre = usuario_modificado.nombre
            register.apelldio= usuario_modificado.apellido
            register.username= usuario_modificado.username
            register.email = usuario_modificado.email
            register.password = usuario_modificado.password
            register.rol= usuario_modificado.rol
            register.departamento=usuario_modificado.departamento
            register.claustro=usuario_modificado.claustro
            self.__session.commit()
        else:
            raise ValueError("El usuario no existe en la base de datis")

    def obtener_registro_por_filtro(self, filtro, valor):
        """
        Obtiene un único registro de usuario de la base de datos por un filtro específico.

        Args:
            filtro (str): El nombre del atributo del modelo (ej. "id", "email", "username")
                          por el cual filtrar.
            valor (any): El valor a buscar.

        Returns:
            Usuario or None: El objeto Usuario si se encuentra un match, de lo contrario, None.
        """
        modelo_usuario = self.__session.query(ModeloUsuario).filter_by(**{filtro:valor}).first()
        return self.__map_modelo_a_entidad(modelo_usuario) if modelo_usuario else None
    
    def eliminar_registro(self, id):
        """
        Elimina un usuario de la base de datos por su ID.

        Args:
            id (int): El ID del usuario a eliminar.

        Raises:
            ValueError: Si el usuario no existe en la base de datos.
            Exception: Cualquier error que ocurra durante la transacción de la base de datos.
        """
        register = self.__session.query(ModeloUsuario).filter_by(id=id).first()
        if register:
            self.__session.delete(register)
            self.__session.commit()
        else:
            raise ValueError("El usuario no existe en la base de datos")
    def __map_entidad_a_modelo(self, entidad: Usuario):
        """
        Mapea un objeto de dominio Usuario a un objeto ModeloUsuario (SQLAlchemy).

        Args:
            entidad (Usuario): El objeto de dominio Usuario.

        Returns:
            ModeloUsuario: La representación del usuario lista para la base de datos.
        """
        return ModeloUsuario(
            id= entidad.id,
            nombre=entidad.nombre,
            apellido=entidad.apellido,
            username=entidad.username,
            email=entidad.email,
            password=entidad.password,
            rol=entidad.rol,
            departamento=entidad.departamento,
            claustro=entidad.claustro
        )
    
    def __map_modelo_a_entidad(self, modelo: ModeloUsuario):
        """
        Mapea un objeto ModeloUsuario (SQLAlchemy) a un objeto de dominio Usuario.

        Args:
            modelo (ModeloUsuario): El modelo de usuario de la base de datos.

        Returns:
            Usuario: La representación del usuario como objeto de dominio.
        """
        return Usuario(
            modelo.id,
            modelo.nombre,
            modelo.apellido,
            modelo.username,
            modelo.email,
            modelo.password,
            modelo.rol,
            modelo.departamento,
            modelo.claustro
            
        )