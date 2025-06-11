class Reclamo:
    def __init__(self, p_id, p_descripcion, p_estado, pd_id_usuario, p_departamento="sin departamento", p_fecha_creacion=None, p_foto=None, p_fecha_resolucion=None):
        self.id= p_id
        self.descripcion=p_descripcion
        self.estado =p_estado
        self.id_usuario= pd_id_usuario
        self.departamento= p_departamento
        self.fecha_creacion = p_fecha_creacion
        self.foto=p_foto
        self.fecha_resolucion=p_fecha_resolucion
    
    @property
    def id(self):
        return self.__id
    
    @property
    def descripcion(self):
        return self.__descripcion
    
    @property
    def estado(self):
        return self.__estado
    
    @property 
    def id_usuario(self):
        return self.__id_usuario
    
    @property
    def departamento(self):
        return self.__departamento
    
    @property
    def fecha_creacion(self):
        return self.__fecha_creacion
    
    @property
    def foto(self):
        return self.__foto
    
    @property
    def fecha_resolucion(self):
        return self.__fecha_resolucion
    
    @id.setter
    def id(self, p_id):
        if p_id is not None and not isinstance(p_id, int):
            raise ValueError("El id debe ser un número entero")
        self.__id=p_id

    @descripcion.setter
    def descripcion(self, p_descripcion):
        if not isinstance(p_descripcion, str) or p_descripcion.strip() == "":
            raise ValueError("La descripcion no puede estar vacía")
        self.__descripcion= p_descripcion.strip()

    @estado.setter
    def estado(self, p_estado):
        if p_estado not in ["pendiente", "resuelto", "en proceso","inválido"]:
            raise ValueError("El estado debe ser 'pendiente', 'resuelto', 'en proceso' o 'invalido'")
        self.__estado=p_estado

    @id_usuario.setter
    def id_usuario(self, p_id_usuario):
        if  p_id_usuario is not None and not isinstance(p_id_usuario, int):
            raise ValueError("El ID de usuario debe ser un número entero")
        self.__id_usuario=p_id_usuario

    @departamento.setter
    def departamento(self, p_departamento):
        print(f"[DEBUG] Setter departamento: {p_departamento}")
        if not isinstance(p_departamento, str) or p_departamento.strip()== "":
            raise ValueError("El departamento no puede estar vacío")
        self.__departamento=p_departamento

    @fecha_creacion.setter
    def fecha_creacion(self, p_fecha_creacion):
        self.__fecha_creacion= p_fecha_creacion

    @foto.setter
    def foto(self, p_foto):
        self.__foto=p_foto

    @fecha_resolucion.setter
    def fecha_resolucion(self, p_fecha_resolucion):
        self.__fecha_resolucion= p_fecha_resolucion

    def calcular_tiempo_resolucion(self):
        if self.fecha_resolucion and self.fecha_creacion:
            return (self.fecha_resolucion - self.fecha_creacion).days
        return None


    def to_dict(self):
        return {
            "id":self.id,
            "descripcion":self.descripcion,
            "estado": self.estado,
            "id_usuario": self.id_usuario,
            "departamento": self.departamento,
            "fecha_creacion": getattr(self, "fecha_creacion", None),
            "fecha_resolucion":self.fecha_resolucion,
            "foto":self.foto
        }
    
    def __str__(self):
        return  f"Reclamo {self.id}: {self.descripcion} (Estado: {self.estado}) "


class Usuario:
    def __init__(self, p_id, p_nombre,p_apellido,p_username, p_email, p_password, rol, p_departamento, p_claustro):
        self.id = p_id
        self.nombre = p_nombre
        self.apellido= p_apellido
        self.username=p_username
        self.email = p_email
        self.password = p_password
        self.rol=rol
        self.departamento= p_departamento or "sin departamento"
        self.claustro=p_claustro

    @property
    def id(self):
        return self.__id
    
    @property
    def nombre(self):
        return self.__nombre
    
    @property
    def apellido(self):
        return self.__apellido
    
    @property 
    def username(self):
        return self.__username
    
    @property
    def email(self):
        return self.__email
    
    @property
    def password(self):
        return self.__password
    
    @property 
    def rol(self):
        return self.__rol
    
    @property
    def departamento(self):
        return self.__departamento
    
    @property
    def claustro(self):
        return self.__claustro
    
    @id.setter
    def id(self, p_id):
        if p_id != None:
            if not isinstance(p_id, int):
                raise ValueError("El id del usuario debe ser un número entero")
            self.__id = p_id
        else:
            self.__id = None
    
    @nombre.setter
    def nombre(self, p_nombre:str):
        if not isinstance(p_nombre, str) or p_nombre.strip() == "":
            raise ValueError("El nombre del usuario debe ser un string y no debe estar vacío")
        self.__nombre = p_nombre.strip()

    @apellido.setter
    def apellido(self, p_apellido:str):
        if not isinstance(p_apellido, str) or p_apellido.strip()=="":
            raise ValueError("El apellido del usuario debe ser un string y no debe estar vacío")
        self.__apellido= p_apellido.strip()

    @username.setter
    def username(self,p_username:str):
        if not isinstance(p_username, str) or p_username.strip()=="":
            raise ValueError("El usuario debe ser un string y no debe estar vacío")
        self.__username= p_username.strip()
        
    @email.setter
    def email(self, p_email:str):
        if not isinstance(p_email, str) or p_email.strip() == "":
            raise ValueError("El email de usuario debe ser un string y no debe estar vacío")
        self.__email = p_email.strip()
        
    @password.setter
    def password(self, password:str):
        self.__password = password

    @rol.setter
    def rol(self, rol:str):
        self.__rol=rol
    
    @departamento.setter
    def departamento(self, p_departamento):
        if not isinstance(p_departamento, str):
            raise ValueError("El departamento debe ser una cadena")
        self.__departamento= p_departamento

    @claustro.setter
    def claustro(self, p_claustro):
        if p_claustro not in ["estudiante", "docente", "pays"]:
            raise ValueError("Claustro Inválido")
        self.__claustro=p_claustro
    def to_dict(self):
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
            