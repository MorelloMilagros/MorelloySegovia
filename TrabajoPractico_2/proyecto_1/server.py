from modules.personas import Estudiante, Profesor
from modules.universidad import Facultad,Curso,Departamento

class SistemaUniversitario():
    def __init__(self):
        self.facultad= Facultad("Facultad de Ciencias")
        self.cargar_datos_iniciales()

    def cargar_datos_iniciales(self):
        try:
            with open('data/profesor.txt', 'r')as archivo:
                for linea in archivo:
                    nombre,dni=linea.strip().split(',')
                    self.facultad.agregar_estudiante(Profesor(nombre,dni))

        except FileNotFoundError:
            print("Archivo profesor.txt no encontrado")


        try:
            with open('data/estudiantes.txt', 'r')as archivo:
                for linea in archivo:
                    nombre,dni=linea.strip.split(',')
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
            opcion = input("Selecciones una opcion: ")

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
        pass
    def contratar_profesor(self):
        pass
    def crear_departamento(self):
        pass
    def crear_curso(self):
        pass
    def inscribir_en_curso(self):
        pass