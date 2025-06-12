from modules.dominio import Reclamo
from modules.repositorio_abstracto import RepositorioAbstracto
from modules.monticulo_binario import MedianHeap
from datetime import datetime, timedelta
from collections import Counter
from nltk.corpus import stopwords
class GestorDeReclamos:
    def __init__(self, repo: RepositorioAbstracto, clasificador=None):
        self.__repo=repo
        self.__numero_reclamos= len(self.__repo.obtener_todos_los_registros())
        self.__clasificador=clasificador

    @property
    def repo(self):
        return self.__repo

    @property
    def numero_reclamos(self):
        return self.__numero_reclamos

    def agregar_nuevo_reclamo(self, descripcion, id_usuario, departamento, p_foto=None):
        if not departamento:
            raise ValueError("El reclamo debe pertenecer a un departamento")
        
        reclamo= Reclamo(None, descripcion, "pendiente", id_usuario, departamento, p_foto=p_foto)
        self.__repo.guardar_registro(reclamo)


    def listar_reclamos(self):
            reclamos = self.__repo.obtener_registros_por_filtros()
            resultado = []
            for r in reclamos:
                r_dict = r.to_dict()
                r_dict['adherentes'] = self.obtener_cantidad_adherentes(r.id)
                resultado.append(r_dict)
            return resultado

    def listar_reclamos_por_departamento(self, departamento, estado=None):
        """
        Devuelve una lista de reclamos filtrados.
        Si se especifica un estado, también filtra por él.
        """
        if not departamento or departamento.strip() == "":
            raise ValueError("El departamento no es válido")

        # Construimos el diccionario de filtros dinámicamente
        filtros = {"departamento": departamento.strip()}    
        if estado:
            filtros["estado"] = estado

        # Una sola llamada eficiente a la base de datos
        reclamos = self.__repo.obtener_registros_por_filtros(**filtros)

        # Procesamos el resultado
        resultado = []
        for r in reclamos:
            r_dict = r.to_dict()
            r_dict['adherentes'] = self.obtener_cantidad_adherentes(r.id)
            resultado.append(r_dict)
        return resultado

    def listar_reclamos_para_usuarios(self):
        """
        Obtiene solo los reclamos con estado 'pendiente'.
        """
        # Llamada eficiente que solo trae los pendientes
        reclamos = self.__repo.obtener_registros_por_filtros(estado="pendiente")
        resultado = []
        for r in reclamos:
            r_dict = r.to_dict()
            r_dict['adherentes'] = self.obtener_cantidad_adherentes(r.id)
            resultado.append(r_dict)
        return resultado

    def actualizar_estado_reclamo(self, id_reclamo, nuevo_estado, dias_resolucion=None):
        reclamo = self.repo.obtener_registro_por_filtro("id", id_reclamo)
        if not reclamo:
            raise ValueError("El reclamo no existe")

        reclamo.estado = nuevo_estado
        
        if nuevo_estado == "resuelto":
            reclamo.fecha_resolucion = datetime.now()
        elif nuevo_estado == "en proceso":
            # --- LÓGICA CORREGIDA ---
            # Ahora es obligatorio que dias_resolucion tenga un valor
            if dias_resolucion is None:
                raise ValueError("Para poner un reclamo 'en proceso', se debe especificar un tiempo de resolución.")
            
            try:
                dias_int = int(dias_resolucion)
                # La consigna especifica un rango de 1 a 15 días
                if not (1 <= dias_int <= 15):
                    raise ValueError("El tiempo de resolución debe estar entre 1 y 15 días.")
                reclamo.fecha_resolucion = datetime.now() + timedelta(days=dias_int)
            except (TypeError, ValueError):
                # Esto atrapa si dias_resolucion no es un número (ej. "abc")
                raise ValueError("El tiempo de resolución debe ser un número entero válido.")
        
        # Si el estado es "pendiente" o "inválido", no se toca la fecha_resolucion
        
        self.repo.modificar_registro(reclamo)

    def eliminar_reclamo(self, id_reclamo):
        if self.__repo.obtener_registro_por_filtro("id", id_reclamo):
            self.__repo.eliminar_registro(id_reclamo)
        else:
            raise ValueError("El reclamo no existe")

    def adherir_a_reclamo(self, id_usuario, id_reclamo):
        self.__repo.adherir_usuario_a_reclamo(id_usuario,id_reclamo)

    def obtener_cantidad_adherentes(self, id_reclamo):
        return self.__repo.contar_adherentes(id_reclamo)

    def obtener_departamentos(self):
        """Devuelve una lista de los nombres de los departamentos con reclamos registrados."""
        modelo_reclamos = self.__repo.obtener_todos_los_registros()

        departamentos = {r.departamento for r in modelo_reclamos if r.departamento}  #Usamos un conjunto para evitar duplicados

        return sorted(departamentos)  #Ordenamos los nombres alfabéticamente


    def obtener_estadisticas(self, departamento):
        """Genera estadisticas de reclamos para un depto especifico"""
        reclamos = self.__repo.obtener_registros_por_filtros(departamento=departamento)
        total=len(reclamos)
        pendientes= sum(1 for r in reclamos if r.estado == "pendiente")
        en_proceso = sum(1 for r in reclamos if r.estado== "en proceso")
        resueltos= sum(1 for r in reclamos if r. estado == "resuelto")
        #Inicio el monticulo binario
        median_heap_resueltos=MedianHeap()
        median_heap_en_proceso= MedianHeap()
        #Se insertan los tiempos de resolucion en la estructura
        for r in reclamos:
            tiempo_resolucion= r.calcular_tiempo_resolucion()
            if r.estado == "resuelto" and tiempo_resolucion is not None:
                median_heap_resueltos.insertar(tiempo_resolucion)
            elif r.estado== "en proceso" and tiempo_resolucion is not None:
                median_heap_en_proceso.insertar(tiempo_resolucion)

        mediana_resueltos= median_heap_resueltos.obtener_mediana() if resueltos > 0 else None
        mediana_en_proceso= median_heap_en_proceso.obtener_mediana() if en_proceso > 0 else None
        #Unir el texto de todos los reclamos del departamento
        texto_completo= ''.join([r.descripcion for r in reclamos])
        #Tokenizar y limpiar el texto
        stop_words_es= set(stopwords.words('spanish'))
        tokens= [palabra.lower() for palabra in texto_completo.split() if palabra.isalpha() and palabra.lower() not in  stop_words_es]
        #Contar las 15 palabras más frecuentes
        contador_palabras= Counter(tokens)
        palabras_clave= contador_palabras.most_common(15)  # Obtiene una lista de tuplas (palabra, frecuencia)
        return {
            "total":total,
            "pendientes": pendientes,
            "en proceso": en_proceso,
            "resueltos":resueltos,
            "mediana resueltos": mediana_resueltos,
            "mediana en proceso": mediana_en_proceso,
            "palabras_clave": palabras_clave
        }
    
    def obtener_reclamo(self, id_reclamo):
      return self.__repo.obtener_registro_por_filtro("id", id_reclamo)

    def clasificar_descripcion(self, descripcion):
        if not self.__clasificador:
            raise ValueError("Clasificador no configurado")
        return self.__clasificador.clasificar([descripcion])[0]

    def buscar_similares(self, descripcion):
        categoria=  self.clasificar_descripcion(descripcion)
        todos= self.__repo.obtener_todos_los_registros()
        similares= [r for r in todos if self.clasificar_descripcion(r.descripcion)== categoria]
        return similares

