class Reclamo:
    def __init__(self, p_id, p_descripcion, p_estado, pd_id_usuario, p_departamento="sin departamento"):
        self.id= p_id
        self.descripcion=p_descripcion
        self.estado =p_estado
        self.id_usuario= pd_id_usuario
        self.departamento= p_departamento
    
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
        if p_estado not in ["pendiente", "resuelto"]:
            raise ValueError("El estado debe ser 'pendiente' o 'resuelto'")
        self.__estado=p_estado

    @id_usuario.setter
    def id_usuario(self, p_id_usuario):
        if  p_id_usuario is not None and not isinstance(p_id_usuario, int):
            raise ValueError("El ID de usuario debe ser un número entero")
        self.__id_usuario=p_id_usuario

    @departamento.setter
    def departamento(self, p_departamento):
        if not isinstance(p_departamento, str) or p_departamento.strip()== "":
            raise ValueError("El departamento no puede estar vacío")
        self.__departamento=p_departamento

    def to_dict(self):
        return {
            "id":self.id,
            "descripcion":self.descripcion,
            "estado": self.estado,
            "id_usuario": self.id_usuario
        }
    
    def __str__(self):
        return  f"Reclamo {self.id}: {self.descripcion} (Estado: {self.estado}) "


class Usuario:
    def __init__(self, p_id, p_nombre, p_email, p_password, rol, p_departamento):
        self.id = p_id
        self.nombre = p_nombre
        self.email = p_email
        self.password = p_password
        self.rol=rol
        self.departamento= p_departamento or "sin departamento"

    @property
    def id(self):
        return self.__id
    
    @property
    def nombre(self):
        return self.__nombre
    
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

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "email": self.email,
            "password": self.password,
            "rol": self.rol,
            "departamento":self.departamento
        }
            