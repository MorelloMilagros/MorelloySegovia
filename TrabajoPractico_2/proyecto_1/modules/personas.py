class Persona():
    def __init__(self, nombre, dni):
        self.__nombre=nombre
        self.__dni=dni

    @property   
    def nombre(self):
        return self.__nombre
    @property
    def dni(self):
        return self.__dni
    
    @nombre.setter 
    def nombre(self,nombre):
        self.__nombre=nombre
    
    @dni.setter
    def dni(self,dni):
        self.__dni=dni

class Profesor(Persona):
    def __init__(self,nombre,dni,departamentos=None):
        super().__init__(nombre,dni)
        self.__departamentos=departamentos if departamentos is not None else []
        self.__cursos_a_cargo=[]
        self.__director_de= None
        
    @property
    def departamentos(self):
        return self.__departamentos
    @property
    def cursos_a_cargo(self):
        return self.__cursos_a_cargo
    
    @property
    def director_de(self):
        return self.__director_de
    

    @director_de.setter
    def director_de(self,departamento):
        if departamento in self.__departamentos:
            self.__director_de=departamento
            departamento.director=self
            

    def agregar_departamento(self, departamento):
        if departamento not in self.__departamentos:
            self.__departamentos.append(departamento)
            departamento.agregar_profesor(self)
            

    def agregar_curso(self,curso):
        if curso not in self.__cursos_a_cargo:
            self.__cursos_a_cargo.append(curso)
            curso.profesor=self
            
class Estudiante(Persona):
    pass
    def __init__(self,nombre,dni,facultades=None):
        super().__init__(nombre,dni)
        self.__cursos=[]
        self.__facultades=facultades if facultades is not None else []
        
    @property
    def cursos(self):
        return self.__cursos
    
    @property
    def facultades(self):
        return self.__facultades
    
    def inscribir_curso(self, curso):
        if curso not in self.__cursos:
            self.__cursos.append(curso)
            curso.agregar_estudiante(self)

    def agregar_facultad(self,facultad):
        if facultad not in self.__facultades:
            self.__facultades.append(facultad)
            facultad.agregar_estudiante(self)

    