from modules.reporte_abstracto import Reporte
from modules.gestor_reclamos import GestorDeReclamos
from modules.graficador_abstracto import Graficador
from modules.monticulo_binario import MedianHeap
from collections import Counter
from nltk.corpus import stopwords

class ReporteConcreto(Reporte):
    """
    Implementación concreta para generar un reporte estadístico de reclamos
    para un departamento específico.
    """
    def __init__(self, gestor_reclamos=GestorDeReclamos, graficador=Graficador):
        """
        Inicializa el generador de reportes con un gestor de reclamos.

        Args:
            gestor_reclamos (GestorDeReclamos): La instancia del gestor
                                               para acceder a los datos de los reclamos.
            graficador(Graficador):
        """
        self.__gestor_reclamos= gestor_reclamos
        self.__graficador= graficador
    
    def generar_reporte(self, **kwargs):
        """Retorna solo las estadísticas numéricas."""
        departamento = kwargs.get("departamento")
        if not departamento:
            raise ValueError("Se requiere un departamento para generar el reporte.")
        
        reclamos = self.__gestor_reclamos.repo.obtener_registros_por_filtros(departamento=departamento)
        return self._calcular_estadisticas(reclamos)

    def _calcular_estadisticas(self, reclamos:list)->dict:
        """
        Genera estadísticas detalladas para los reclamos de un departamento específico.

        Incluye el número total de reclamos, conteos por estado (pendientes,
        en proceso, resueltos), la mediana del tiempo de resolución para reclamos
        resueltos y en proceso (utilizando `MedianHeap`), y las 15 palabras
        más frecuentes en las descripciones de los reclamos (excluyendo stopwords).

        Args:
            departamento (str): El departamento para el cual generar las estadísticas.

        Returns:
            dict: Un diccionario con las siguientes claves:
                  - "total" (int): Cantidad total de reclamos.
                  - "pendientes" (int): Cantidad de reclamos pendientes.
                  - "en proceso" (int): Cantidad de reclamos en proceso.
                  - "resueltos" (int): Cantidad de reclamos resueltos.
                  - "inválidos" (int): Cantidad de reclamos inválidos.
                  - "mediana resueltos" (float or None): Mediana del tiempo de resolución de reclamos resueltos.
                  - "mediana en proceso" (float or None): Mediana del tiempo de resolución de reclamos en proceso.
                  - "palabras_clave" (list): Una lista de tuplas (palabra, frecuencia)
                                            de las 15 palabras más frecuentes.
        """
        total = len(reclamos)
        pendientes = sum(1 for r in reclamos if r.estado == "pendiente")
        en_proceso = sum(1 for r in reclamos if r.estado == "en proceso")
        resueltos = sum(1 for r in reclamos if r.estado == "resuelto")
        invalidos = sum(1 for r in reclamos if r.estado == "inválido")

        # Se inicializan ambos montículos para las medianas
        median_heap_resueltos = MedianHeap()
        median_heap_en_proceso = MedianHeap()

        for r in reclamos:
            tiempo = r.calcular_tiempo_resolucion()
            if tiempo is not None:
                if r.estado == "resuelto":
                    median_heap_resueltos.insertar(tiempo)
                elif r.estado == "en proceso":
                    # Para reclamos 'en proceso', el tiempo_resolucion es el tiempo estimado hasta la fecha objetivo
                    # La mediana se calcula sobre la duración estimada desde la creación hasta la fecha_resolucion asignada
                    # Es importante que calcular_tiempo_resolucion retorne los días restantes o transcurridos.
                    # Aquí, se asume que retorna los días desde la creación si fecha_resolucion es la estimada.
                    median_heap_en_proceso.insertar(tiempo)

        # Manejo de casos donde no hay elementos para calcular la mediana
        mediana_resueltos = median_heap_resueltos.obtener_mediana() if resueltos > 0 else None
        mediana_en_proceso = median_heap_en_proceso.obtener_mediana() if en_proceso > 0 else None

        # Unir el texto de todos los reclamos del departamento para la nube de palabras
        texto_completo = ' '.join([r.descripcion for r in reclamos])
        
        # Tokenizar y limpiar el texto
        # Se descarga 'spanish' stopwords si no está disponible (ya manejado en text_vectorizer.py)
        stop_words_es = set(stopwords.words('spanish'))
        tokens = [palabra.lower() for palabra in texto_completo.split() if palabra.isalpha() and palabra.lower() not in stop_words_es]
        
        # Contar las 15 palabras más frecuentes
        contador_palabras = Counter(tokens)
        palabras_clave = contador_palabras.most_common(15) # Obtiene una lista de tuplas (palabra, frecuencia)

        return {
            "total": total, 
            "pendientes": pendientes, 
            "en_proceso": en_proceso,
            "resueltos": resueltos, 
            "invalidos": invalidos,
            "mediana_resueltos": mediana_resueltos,
            "mediana_en_proceso": mediana_en_proceso, 
            "palabras_clave": palabras_clave
        }
    
    def generar_visualizacion(self, tipo_grafico: str, **kwargs) -> bytes:
        """
        Delega la creación de un gráfico específico al graficador.
        Este método actúa como un despachador (dispatcher).
        """
        departamento = kwargs.get("departamento")
        if not departamento:
            raise ValueError("Se requiere un departamento para generar la visualización.")

        reclamos = self.__gestor_reclamos.repo.obtener_registros_por_filtros(departamento=departamento)
        stats = self._calcular_estadisticas(reclamos)
        
        datos_estados = {
            "Pendientes": stats["pendientes"], "En Proceso": stats["en_proceso"],
            "Resueltos": stats["resueltos"], "Inválidos": stats["invalidos"]
        }

        if tipo_grafico == 'barras':
            return self.__graficador.crear_grafico_barras(
                datos_estados,
                f"Estado de Reclamos en {departamento}", "Estado", "Cantidad")
        
        elif tipo_grafico == 'torta':
            return self.__graficador.crear_grafico_torta(
                datos_estados,
                f"Proporción de Estados en {departamento}")
        
        elif tipo_grafico == 'nube':
            return self.__graficador.crear_nube_palabras(
                stats["palabras_clave"],
                f"Palabras Frecuentes en Reclamos de {departamento}")
        
        else:
            raise ValueError(f"Tipo de gráfico '{tipo_grafico}' no soportado.")