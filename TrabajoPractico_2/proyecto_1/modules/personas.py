class Persona:
    #Clase base abstracta
    def __init__(self, nombre, dni):
        self.__nombre=nombre
        self.__dni=dni

    @property   
    def nombre(self):
        #Devuelve el nombre de la persona
        return self.__nombre
    @property
    def dni(self):
        #Devuelve el dni de la persona
        return self.__dni
    
    @nombre.setter 
    def nombre(self,nombre):
        #Permite modificar el nombre
        self.__nombre=nombre
    
    @dni.setter
    def dni(self,dni):
        #Permite modificar el dni
        self.__dni=dni

    def __str__(self):
        return f"{self.nombre} ({self.dni})"
    
class Profesor(Persona):
    #Representa a un profesor. Puede estar a cargo de varios cursos y formar parte de varios departamentos. También puede ser director de un único departamento.
    def __init__(self,nombre,dni,departamentos=None):
        super().__init__(nombre,dni)
        self.__departamentos=departamentos if departamentos is not None else []
        self.__curso_donde_dicta=[]
        self.__director_de= None
        
    @property
    def departamentos(self):
        #Lista de departamentos a los que pertenece el profesor
        return self.__departamentos
    @property
    def curso_donde_dicta(self):
        #Lista de cursos de los cuales esta a cargo el profesor
        return self.__curso_donde_dicta
    
    @property
    def director_de(self):
        #Departamento del cual esta a cargo el profesor
        return self.__director_de
    

    @director_de.setter
    def director_de(self,departamento):
        #Asigna al profesor como director de un departamento
        if departamento in self.__departamentos:
            self.__director_de=departamento
            departamento.director=self
            

    def agregar_departamento(self, departamento):
        #Agrega un departamento al profesor, y actualiza el departamento
        if departamento not in self.__departamentos:
            self.__departamentos.append(departamento)
            departamento.agregar_profesor(self)
            
    @curso_donde_dicta.setter
    def curso_donde_dicta(self,curso):
        if self.__curso_donde_dicta!=curso:
            self.__curso_donde_dicta=curso
            curso.agregar_profesor(self)

            
class Estudiante(Persona):
    #Representa a un estudiante. Puede inscribirse en cursos y pertenecer a múltiples facultades.
    def __init__(self,nombre,dni,facultades=None):
        super().__init__(nombre,dni)
        self.__cursos=[]
        
    @property
    def cursos(self):
        #Lista de cursos a los que pertenece el estudiante
        return self.__cursos
    
    def inscribir_curso(self, curso):
        #Inscribe al estudiante en un curso, actuliza el curso
        if curso not in self.__cursos:
            self.__cursos.append(curso)
            curso.agregar_estudiante(self)