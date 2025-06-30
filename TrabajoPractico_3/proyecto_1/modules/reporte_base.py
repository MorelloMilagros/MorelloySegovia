from abc import ABC
from collections import Counter
from datetime import datetime
from nltk.corpus import stopwords
from modules.gestor_reclamos import GestorDeReclamos
from modules.graficador_abstracto import Graficador
from modules.monticulo_binario import MedianHeap
from modules.reporte_abstracto import Reporte

class ReporteBase(Reporte, ABC):
    """
    Clase base para los reportes. Contiene la lógica compartida para
    obtener y calcular las estadísticas de los reclamos.
    """
    def __init__(self, gestor_reclamos: GestorDeReclamos, graficador: Graficador):
        """
        Constructor que asegura que las dependencias se guarden como atributos.
        """
        self._gestor_reclamos = gestor_reclamos
        self._graficador = graficador

    def _obtener_datos(self, departamento: str) -> tuple:
        """Obtiene los reclamos y calcula las estadísticas."""
        reclamos_dicts = self._gestor_reclamos.listar_reclamos_por_departamento(departamento)
        stats = self._calcular_estadisticas(reclamos_dicts)
        return reclamos_dicts, stats

    def _calcular_estadisticas(self, reclamos: list[dict]) -> dict:
        """
        Procesa una lista de diccionarios de reclamos y devuelve estadísticas.
        """
        total = len(reclamos)
        pendientes = sum(1 for r in reclamos if r.get('estado') == "pendiente")
        en_proceso = sum(1 for r in reclamos if r.get('estado') == "en proceso")
        resueltos = sum(1 for r in reclamos if r.get('estado') == "resuelto")
        invalidos = sum(1 for r in reclamos if r.get('estado') == "inválido")

        median_heap_resueltos = MedianHeap()
        median_heap_en_proceso = MedianHeap()

        for r in reclamos:
            if r.get('fecha_resolucion') and r.get('fecha_creacion'):
                fecha_creacion = r['fecha_creacion']
                fecha_resolucion = r['fecha_resolucion']
                if isinstance(fecha_creacion, datetime) and isinstance(fecha_resolucion, datetime):
                    tiempo = (fecha_resolucion - fecha_creacion).days
                    if r['estado'] == "resuelto":
                        median_heap_resueltos.insertar(tiempo)
                    elif r['estado'] == "en proceso":
                        median_heap_en_proceso.insertar(tiempo)

        mediana_resueltos = median_heap_resueltos.obtener_mediana() if resueltos > 0 else None
        mediana_en_proceso = median_heap_en_proceso.obtener_mediana() if en_proceso > 0 else None

        texto_completo = ' '.join([r['descripcion'] for r in reclamos])
        stop_words_es = set(stopwords.words('spanish'))
        tokens = [p.lower() for p in texto_completo.split() if p.isalpha() and p.lower() not in stop_words_es]
        palabras_clave = Counter(tokens).most_common(15)

        return {
            "total": total, "pendientes": pendientes, "en_proceso": en_proceso,
            "resueltos": resueltos, "invalidos": invalidos,
            "mediana_resueltos": mediana_resueltos, "mediana_en_proceso": mediana_en_proceso,
            "palabras_clave": palabras_clave
        }
