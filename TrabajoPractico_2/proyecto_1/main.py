from modules.personas import Estudiante, Profesor
from modules.universidad import Facultad,Curso,Departamento
import os
    
class SistemaUniversitario():
    """Clase principal que gestiona el sistema de información universitaria."""

    def __init__(self):
        """Inicializa el sistema con una facultad base e intenta cargar datos iniciales de estudiantes y profesores."""
        self.facultad = Facultad("Facultad de Ciencias")
        self.cargar_datos_iniciales()

    def cargar_datos(self, archivo, tipo):
    #Carga datos desde un archivo de texto y los agrega a la facultad.
        try:
            with open(archivo, 'r', encoding='utf-8') as f:
                lineas = f.readlines()
                if not lineas:
                    print(f"Advertencia: {archivo} está vacío.")
                    return
                
                for linea in lineas:
                    datos = linea.strip().split(',')

                    # Validaciones generales
                    if tipo in ["profesor", "estudiante"] and len(datos) != 2:
                        print(f"Advertencia: Línea incorrecta en {archivo}, ignorando: {linea.strip()}")
                        continue
                    
                    if tipo == "profesor":
                        nombre, dni = datos
                        if dni.isdigit():
                            self.facultad.agregar_profesor(Profesor(nombre, dni))
                        else:
                            print(f"Advertencia: DNI inválido en {archivo} ({dni}), ignorando entrada.")

                    elif tipo == "estudiante":
                        nombre, dni = datos
                        if dni.isdigit():
                            self.facultad.agregar_estudiante(Estudiante(nombre, dni))
                        else:
                            print(f"Advertencia: DNI inválido en {archivo} ({dni}), ignorando entrada.")

                    elif tipo == "departamento":
                        if len(datos) != 3:
                            print(f" Advertencia: Línea incorrecta en {archivo}, ignorando: {linea.strip()}")
                            continue
                        nombre_depto, nombre_facultad, director_dni = datos
                        #  Buscar si el departamento ya existe por nombre
                        departamento_existente = next((d for d in self.facultad.departamentos if d.nombre == nombre_depto), None)
                        
                        if departamento_existente:
                            print(f" Departamento '{nombre_depto}' ya estaba en memoria. No se duplica.")
                            continue  # Evitar agregarlo nuevamente

                        nuevo_depto = Departamento(nombre_depto, self.facultad)
                        print(f" Departamento '{nombre_depto}' agregado correctamente.")

                        # Asignar director si existe
                        if director_dni != "None":
                            profesor = next((prof for prof in self.facultad.profesores if prof.dni == director_dni), None)
                            if profesor:
                                nuevo_depto.director = profesor

                    elif tipo == "curso":
                        if len(datos) != 3:
                            continue
                        nombre_curso, nombre_departamento, profesor_dni = datos
                        departamento = next((d for d in self.facultad.departamentos if d.nombre == nombre_departamento), None)
                        profesor = next((p for p in self.facultad.profesores if p.dni == profesor_dni), None) if profesor_dni != "None" else None

                        if departamento:
                            Curso(nombre_curso, departamento, profesor)
                    elif tipo == "inscripcion":
                        if len(datos) != 3:
                            print(f"⚠️ Línea incorrecta en {archivo}, ignorando: {linea.strip()}")
                            continue

                        dni_estudiante, nombre_curso, nombre_departamento = datos
                        estudiante = next((e for e in self.facultad.estudiantes if e.dni == dni_estudiante), None)
                        curso = next((c for d in self.facultad.departamentos if d.nombre == nombre_departamento for c in d.cursos if c.nombre == nombre_curso), None)

                        if estudiante and curso:
                            curso.agregar_estudiante(estudiante)
                            print(f"✅ Inscripción restaurada: {estudiante.nombre} en {curso.nombre}")

        except FileNotFoundError:
            print(f"Error: Archivo {archivo} no encontrado.")

    def cargar_datos_iniciales(self):
    #Carga automáticamente estudiantes, profesores, departamentos y cursos desde archivos.
        if not os.path.exists('data'):
            os.makedirs('data')

        archivos = [
            ("data/profesores.txt", "profesor"),
            ("data/estudiantes.txt", "estudiante"),
            ("data/departamentos.txt", "departamento"),
            ("data/cursos.txt", "curso"),
            ("data/inscripciones.txt", "inscripcion")
        ]

        for archivo, tipo in archivos:
            self.cargar_datos(archivo, tipo)

    def menu(self):
        #Muestra el menú principal del sistema.
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
        #Ejecuta el menú de forma iterativa hasta que el usuario elija salir.
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
        #Permite registrar un nuevo estudiante desde la consola y lo guarda en el archivo de texto correspondiente (estudiantes.txt).
        print("---Incribir Alumno---")
        nombre=input("Ingrese su nombre completo: ").strip()
        #Validar que haya nombre
        while not nombre:
            print("ERROR: El nombre no puede estar vacío.")
            nombre = input("Ingrese su nombre completo: ").strip()
        dni=input("Ingrese su DNI: ").strip()
        #Validar que el dni consista en numeros
        while not dni.isdigit():
            print("ERROR: El DNI debe contener solo números.")
            dni = input("Ingrese su DNI: ").strip()
        if any(i.dni== dni for i in self.facultad.estudiantes):
            print("ERROR!. Ya existe un estudiante con ese DNI")
            return 
        
        estudiante=Estudiante(nombre,dni)
        self.facultad.agregar_estudiante(estudiante)

        with open('data/estudiantes.txt', 'a', encoding='utf-8')as f:
            f.write(f"\n{nombre},{dni}")
        print(f"\n Estudiante {nombre} inscripto/a correctamente en {self.facultad.nombre}")

        print(f"\nLista de estudiantes actuales:")
        for e in self.facultad.estudiantes:
            print(f"- {e.nombre}, {e.dni} ")

    def contratar_profesor(self):
        #Permite registrar un nuevo profesor desde consola y lo guarda en el archivo correspondiente (estudiantes.txt).
        print("---Contratacion de profesor---")
        nombre=input("Nombre completo: ").strip()
        while not nombre:
            print("ERROR: El nombre no puede estar vacío.")
            nombre = input("Nombre completo: ").strip()
        dni=input("Ingrese el DNI: ").strip()
        while not dni.isdigit():
            print("ERROR: El DNI debe contener solo números.")
            dni = input("Ingrese su DNI: ").strip()
        if any(p.dni== dni for p in self.facultad.profesores):
            print("Error: Ya existe un profesor con ese DNI")
            return  
        
        profesor=Profesor(nombre,dni)
        self.facultad.agregar_profesor(profesor)

        with open('data/profesores.txt', 'a', encoding='utf-8')as f:
            f.write(f"\n{nombre},{dni}")
        print(f"\n profesor {nombre} contratado correctamente")
        print("\nLista de profesores actuales:")
        for p in self.facultad.profesores:
            print(f"- {p.nombre} ({p.dni})")

    def crear_departamento(self): 
        #Permite crear un departamento y asignar un director correctamente.
        print("---Crear Departamento---")
        if not self.facultad.profesores:
            print("Error: No hay profesores disponibles para asignar a un departamento")
            return

        nombre = input("Nombre del departamento: ")
        if any(d.nombre == nuevo_depto.nombre for d in self.facultad.departamentos):
            print(f"Advertencia: Departamento '{nuevo_depto.nombre}' ya existe.")
            return
        print("Profesores disponibles: ")
        for i, profesor in enumerate(self.facultad.profesores, 1):
            print(f"{i}. {profesor.nombre}")

        try:
            opcion = int(input("Seleccione el director (número): ")) - 1
            director = self.facultad.profesores[opcion]
        except (ValueError, IndexError):
            print("Selección no válida")
            return 

        nuevo_depto = Departamento(nombre, self.facultad)
        if any(depto.director == director for depto in self.facultad.departamentos):
            print(f"Error: {director.nombre} ya es director de otro departamento.")
            print(f"Departamento '{nombre}' se ha creado correctamente, pero sin director.")
        else:
            nuevo_depto.agregar_profesor(director)  # Asegurar que el director pertenezca al departamento
            nuevo_depto.director = director  # Asignar director si la restricción lo permite
            print(f"Departamento '{nombre}' creado exitosamente con director: {director.nombre}")
        # Guardar en 'data/departamentos.txt'
        with open('data/departamentos.txt', 'a', encoding='utf-8') as f:
            director_dni = nuevo_depto.director.dni if nuevo_depto.director else "None"
            f.write(f"{nuevo_depto.nombre},{nuevo_depto.facultad.nombre},{director_dni}\n")

        print("\nDepartamentos actuales:")
        for depto in self.facultad.departamentos:
            director_actual = depto.director.nombre if depto.director else "Sin director"
            print(f"- {depto.nombre} (Director: {director_actual})")
            
    def crear_curso(self):
        #Permite crear un nuevo curso en un departamento existente y asignarle un profesor.

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
        if any(curso.nombre == nombre_curso for curso in departamento.cursos):
            print("Ya existe un curso con ese nombre en este departamento.")
            return
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
            #prof_nombre = profesor.nombre if profesor else "None"
            prof_dni = profesor.dni if profesor else "None"
            f.write(f"{nombre_curso},{depto_nombre},{prof_dni}\n")

        print(f"\n Nuevo curso {nombre_curso} creado correctamente en {departamento.nombre}")
        if profesor:
            print(f"Profesor asignado: {profesor.nombre}")

        print("\n Cursos del departamento:")
        for curso in departamento.cursos:
            print(f"- {curso.nombre} ({curso.profesor.nombre if curso.profesor else 'Sin profesor'})")

    def inscribir_en_curso(self):
        #Permite inscribir un estudiante ya existente a un curso disponible.
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
        with open('data/inscripciones.txt', 'a', encoding='utf-8') as f:
            f.write(f"{estudiante.dni},{curso.nombre},{curso.departamento.nombre}\n")
        print(f"\n {estudiante.nombre} inscrito exitosamente en {curso.nombre}")
        print("\nLista de estudiantes en el curso:")
        for est in curso.estudiantes:
            print(f"- {est.nombre} ({est.dni})")

if __name__ == "__main__":
    sistema = SistemaUniversitario()
    sistema.ejecutar()