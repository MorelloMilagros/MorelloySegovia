from modules.personas import Estudiante, Profesor
from modules.universidad import Facultad,Curso,Departamento
import os
class SistemaUniversitario():
    def __init__(self):
        self.facultad= Facultad("Facultad de Ciencias")
        self.cargar_datos_iniciales()

    def cargar_datos_iniciales(self):
        if not os.path.exists('data'):
            os.makedirs('data')
        try:
            with open('data/profesor.txt', 'r')as archivo:
                for linea in archivo:
                    nombre,dni=linea.strip().split(',')
                    self.facultad.agregar_profesor(Profesor(nombre,dni))

        except FileNotFoundError:
            print("Archivo profesor.txt no encontrado")


        try:
            with open('data/estudiantes.txt', 'r')as archivo:
                for linea in archivo:
                    nombre,dni=linea.strip().split(',')
                    self.facultad.agregar_estudiante(Estudiante(nombre,dni))
        except FileNotFoundError:
            print("Archivo estudiantes.txt no encontrado")

    def menu(self):
        pass
        print("##########################################")
        print("#  Sistema de Información Universitaria  #")
        print("##########################################")
        print("Elige una opción:")
        print("1) Inscribir alumno")
        print("2) Contratar profesor")
        print("3) Crear departamento nuevo")
        print("4) Crear curso nuevo")
        print("5) Inscribir estudiante a un curso")
        print("6) Salir")

    def ejecutar(self):
        while True:
            self.menu()
            opcion = input("Seleccione una opcion: ")

            if opcion =="1":
                self.inscribir_alumno()
            elif opcion =="2":
                self.contratar_profesor()
            elif opcion =="3":
                self.crear_departamento()
            elif opcion =="4":
                self.crear_curso()
            elif opcion =="5":
                self.inscribir_en_curso()
            elif opcion =="6":
                print("Adiós")
                break
            else:
                print("Opcion invalida. Intente nuevamente.")
    
    def inscribir_alumno(self):
        print("---Incribir Alumno---")
        nombre=input("Imgrese su nombre completo: ")
        dni=input("Ingrese su DNI: ")

        if any(i.dni== dni for i in self.facultad.estudiantes):
            print("ERROR!. Ya existe un estudiante con ese DNI")
            return 
        
        estudiante=Estudiante(nombre,dni)
        self.facultad.agregar_estudiante(estudiante)

        with open('data/estudiantes.txt', 'a', encoding='utf-8')as f:
            f.write(f"\n{nombre},{dni}\n")
        print(f"\n Estudiante {nombre} inscripto/a correctamente en {self.facultad.nombre}")
    
    def contratar_profesor(self):
        print("---Contratacion de profesor---")
        nombre=input("Nombre completo: ")
        dni=input("Ingrese el DNI: ")

        if any(p.dni== dni for p in self.facultad.profesores):
            print("Error: Ya existe un profesor con ese DNI")
            return  
        
        profesor=Profesor(nombre,dni)
        self.facultad.agregar_profesor(profesor)

        with open('data/profesor.txt', 'a', encoding='utf-8')as f:
            f.write(f"{nombre} , {dni}\n")
        print(f"\n profesor {nombre} contratado correctamente")

    def crear_departamento(self):
        print("---Crear Departamento---")
        if not self.facultad.profesores:
            print("Error: No hay profesores disponibles para asignar a un departamento")
            return
        nombre= input("Nombre del departamento: ")

        print("Profesores disponibles: ")
        for i, profesor in enumerate(self.facultad.profesores,1):
            print(f"{i}. {profesor.nombre}")

        try:
            opcion=int(input("Seleccione el director (numero): "))-1
            director=self.facultad.profesores[opcion]
        except (ValueError, IndexError):
            print("Seleccion noo válida")
            return 
        
        nuevo_depto= Departamento(nombre, self.facultad)
        nuevo_depto.director=director

        print(f"\n Departamento '{nombre}' creado exitosamente.")
        print(f"Director asignado: {director.nombre}")
        print("\n Departamentos actuales:")
        for depto in self.facultad.departamentos:
            print(f"- {depto.nombre} (Director: {depto.director.nombre if depto.director else 'Sin director'})")
    
    
    def crear_curso(self):
        pass
        print("----Crear Curso---")
        if not self.facultad.departamentos:
            print("Error: No hay departamentos disponibles")
            return
        print("Departamentos Disponibles:")
        for i, depto in enumerate(self.facultad.departamentos,1):
            print(f"{i}. {depto.nombre}")
        
        try:
            opcion_depto=int(input("Seleccione un departamento (numero): "))-1
            departamento= self.facultad.departamentos[opcion_depto]
        except (ValueError, IndexError):
            print("Seleccion no valida")
            return
        nombre_curso= input("Nombre del curso: ")
        print("\n Profesores disponibles:")
        profesores_depto=departamento.profesores
        if not profesores_depto:
            print("No hay profesores disponbibles en este departamento")
            profesor=None
        else:
            for i, prof in enumerate(profesores_depto, 1):
                print(f"{i}. {prof.nombre}")
            opcion_prof= input("Seleccione un prfesor (numero) o enter para ninguno")
            if opcion_prof:
                try:
                    profesor=profesores_depto[int(opcion_prof)-1]
                except (ValueError,IndexError):
                    print("Seleccion no valida, asignando sin profesor")
                    profesor=None
            else:
                profesor=None
        nuevo_curso= Curso(nombre_curso, departamento, profesor)

        with open('data/cursos.txt', 'a', encoding='utf-8') as f:
            depto_nombre = departamento.nombre
            prof_nombre = profesor.nombre if profesor else "None"
            f.write(f"{nombre_curso},{depto_nombre},{prof_nombre}\n")

        print("\n Nuevo curso {nombre_curso} creado correctamente en {departamento.nombre}")
        if profesor:
            print(f"Profesor asignado: {profesor.nombre}")

        print("\n Cursos del departamento:")
        for curso in departamento.cursos:
            print(f"- {curso.nombre} ({curso.profesor.nombre if curso.profesor else 'Sin profesor'})")


    def inscribir_en_curso(self):
        pass
        print("--- Inscripción a Curso ---")
        if not self.facultad.estudiantes:
            print("Error: No hay estudiantes registrados")
            return
        
        if not any(depto.cursos for depto in self.facultad.departamentos):
            print("Error: No hay cursos disponibles")
            return
        
        print("Estudiantes disponibles:")
        for i, estudiante in enumerate(self.facultad.estudiantes, 1):
            print(f"{i}. {estudiante.nombre}")
        
        try:
            opcion_est = int(input("Seleccione estudiante (número): ")) - 1
            estudiante = self.facultad.estudiantes[opcion_est]
        except (ValueError, IndexError):
            print("Selección no válida")
            return
        
        cursos_disponibles = []
        for depto in self.facultad.departamentos:
            cursos_disponibles.extend(depto.cursos)
        
        print("\n Cursos disponibles:")
        for i, curso in enumerate(cursos_disponibles, 1):
            print(f"{i}. {curso.nombre} ({curso.departamento.nombre})")
        
        try:
            opcion_curso = int(input("Seleccione curso (número): ")) - 1
            curso = cursos_disponibles[opcion_curso]
        except (ValueError, IndexError):
            print("Selección no válida")
            return
        
        if estudiante in curso.estudiantes:
            print(f"Error: El estudiante ya está inscrito en este curso")
            return
        
        curso.agregar_estudiante(estudiante)
        print(f"\n {estudiante.nombre} inscrito exitosamente en {curso.nombre}")
    
if __name__ == "__main__":
    sistema = SistemaUniversitario()
    sistema.ejecutar()