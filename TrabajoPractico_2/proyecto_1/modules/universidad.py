class Facultad:
    #Representa una facultad. Contiene departamentos, profesores y estudiantes.
    def __init__(self, nombre):
        self.__nombre=nombre
        self.__departamentos=[]
        self.__estudiantes=[]
        self.__profesores=[]

    @property
    def nombre(self):
        return self.__nombre
    @property
    def departamentos(self): 
        return self.__departamentos
    @property 
    def estudiantes(self):
        return self.__estudiantes
    @property
    def profesores(self):
        return self.__profesores
    
    def agregar_departamento(self,departamento):
        #Agrega un departamento a la facultad
        if departamento not in self.__departamentos:
            self.__departamentos.append(departamento)
            departamento.facultad= self

    def agregar_estudiante(self, estudiante):
        #Agrega un estudiante a la facultad
        if estudiante not in self.__estudiantes:
            self.__estudiantes.append(estudiante)

    def agregar_profesor(self, profesor):
        #Agrega un profesor a la facultad
        if profesor not in self.__profesores:
            self.__profesores.append(profesor)
            
    def listar_departamentos(self):
        #Devuelve una lista con los departamentos que pertenecen a la facultad
        return [depto.nombre for depto in self.__departamentos]
    
    def listar_estudiantes(self):
        #Devuelve una lista de estudiantes que pertenecen a la facultad
        return [str(est) for est in self.__estudiantes]
    
    def __str__(self):
        return f"Facultad de {self.nombre}"
    

class Departamento:
    #Representa un departamento. Pertenece a una única facultad, tiene un director, cursos y profesores asociados
    def __init__(self, nombre, facultad):
        self.__nombre=nombre
        self.__facultad=facultad
        self.__cursos=[]
        self.__profesores=[]
        self.__director=None
        facultad.agregar_departamento(self)

    @property
    def nombre(self):
        return self.__nombre
    @property 
    def facultad(self):
        return self.__facultad
    @facultad.setter
    def facultad(self,facultad):
        if facultad!=self.__facultad:
             if self.__facultad:
                self.__facultad.departamentos.remove(self)
        self.__facultad=facultad
        facultad.agregar_departamento(self)

    @property
    def cursos(self):
        return self.__cursos
    @property
    def profesores(self):
        return self.__profesores
    @property
    def director(self):
        return self.__director
    
    @director.setter
    def director(self,profesor):
        #Asigna un director al departamento, removiendo a su vez al anterior si es que existe
        if self.__director:
            self.__director.__director_de=None
        self.__director=profesor
        profesor.__director_de=self

    def agregar_profesor(self,profesor):
        #Agrega un profesor al departamento
        if profesor not in self.__profesores:
            self.__profesores.append(profesor)
            profesor.agregar_departamento(self)
    
    def agregar_curso(self,curso):
        #Agrega un curso al departamento
        if curso not in self.__cursos:
            self.__cursos.append(curso)
    
    def listar_profesores(self):
        return [str(prof) for prof in self.__profesores]
    
    def listar_cursos(self):
        return [curso.nombre for curso in self.__cursos]
    
    def __str__(self):
        return f"Departamento de {self.nombre} ({self.facultad.nombre})"

class Curso:
    #Representa un curso. Tiene un nombre, pertenece a un departamento, puede tener un profesor asignado y varios estudiantes inscritos.
    def __init__(self, nombre,departamento, profesores=None):
        self.__nombre=nombre
        self.__profesores=profesores if profesores is not None else[]
        self.__departamento=departamento
        self.__estudiantes=[]
        departamento.agregar_curso(self)
        
    @property
    def nombre(self):
        return self.__nombre
    @property
    def profesores(self):
        return self.__profesores
    @property
    def departamento(self):
        return self.__departamento
    @property
    def estudiantes(self):
        return self.__estudiantes

    def agregar_profesor(self,profesor):
        #Agrega un profesor al curso y actualiza si es necesario
        if profesor not in self.__profesores:
            self.__profesores.append(profesor)
            profesor.curso_donde_dicta=self

    
    def agregar_estudiante(self, estudiante):
        #Agrega al estudiante al curso y actualiza al estudiante
        if estudiante not in self.__estudiantes:
            self.__estudiantes.append(estudiante)
            if self not in estudiante.cursos:
                estudiante.inscribir_curso(self)

    def listar_estudiantes(self):
        return [str(est) for est in self.__estudiantes]
    
    def __str__(self):
        profesor_nombre = self.profesor.nombre if self.profesor else "Sin profesor asignado"
        return f"Curso: {self.nombre} - Profesor: {profesor_nombre}"