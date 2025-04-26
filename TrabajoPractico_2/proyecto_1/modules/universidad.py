class Facultad():
    def __init__(self, nombre):
        self.__nombre=nombre
        self.__departamentos=[]
        self.__estudiantes=[]

    @property
    def nombre(self):
        return self.__nombre
    @property
    def departamentos(self):
        return self.__departamentos
    @property 
    def estudiantes(self):
        return self.__estudiantes
    
    def agregar_departamento(self,departamento):
        if departamento not in self.__departamentos:
            self.__departamentos.append(departamento)
            departamento.facultad= self

    def agregar_estudiante(self, estudiante):
        if estudiante not in self.__estudiantes:
            self.__estudiantes.append(estudiante)
            estudiante.agregar_facultad(self)

    def listar_departamentos(self):
        return [depto.nombre for depto in self.__departamentos]
    
    def listar_estudiantes(self):
        return [str(est) for est in self.__estudiantes]
    
    def __str__(self):
        return f"Facultad de {self.nombre}"
    

class Departamento():
    def __init__(self, nombre, facultad):
        pass
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
        if self.__director:
            self.__director.director_de=None
        self.director=profesor
        profesor.director_de=self

    def agregar_profesor(self,profesor):
        if profesor not in self.__profesores:
            self.__profesores.append(profesor)
            profesor.agregar_departamento(self)
    
    def agregar_curso(self,curso):
        if curso not in self.__cursos:
            self.__cursos.append(curso)
    
    def listar_profesores(self):
        return [str(prof) for prof in self.__profesores]
    
    def listar_cursos(self):
        return [curso.nombre for curso in self.__cursos]
    
    def __str__(self):
        return f"Departamento de {self.nombre} ({self.facultad.nombre})"

class Curso():
    pass
    def __init__(self, nombre,departamento, profesor=None):
        self.__nombre=nombre
        self.__profesor=None
        self.__departamento=departamento
        self.__estudiantes=[]
        departamento.agregar_curso(self)
        self.profesor=profesor
        pass

    @property
    def nombre(self):
        return self.__nombre
    @property
    def profesor(self):
        return self.__profesor
    @property
    def departamento(self):
        return self.__departamento
    @property
    def estudiantes(self):
        return self.__estudiantes

    @profesor.setter
    def profesor(self,profesor):
        if profesor==self.__profesor:
            return
        
        if self.__profesor:
            self.__profesor.cursos_a_cargo.remove(self)
        self.__profesor=profesor
        if profesor:
            profesor.agregar_curso(self)
    
    def agregar_estudiante(self, estudiante):
        if estudiante not in self.__estudiantes:
            self.__estudiantes.append(estudiante)
            if self not in estudiante.cursos:
                estudiante.inscribir_curso(self)

    def listar_estudiantes(self):
        return [str(est) for est in self.__estudiantes]
    
    def __str__(self):
        profesor_nombre = self.profesor.nombre if self.profesor else "Sin profesor asignado"
        return f"Curso: {self.nombre} - Profesor: {profesor_nombre}"