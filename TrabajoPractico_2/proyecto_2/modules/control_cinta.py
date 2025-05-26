from typing import Dict, Type, Optional, Any
from modules.detector_alimento import DetectorAlimento
from modules.cajon import Cajon
from modules.alimento import Alimento, Kiwi, Manzana, Papa, Zanahoria

# --- Clase de Control de la Cinta Transportadora ---
class ControlCinta:
    """Orquesta el llenado de cajones con alimentos detectados."""
    
    # Mapa de clases como atributo de clase (privado)
    _MAPA_CLASES_ALIMENTO: Dict[str, Type[Alimento]] = {
        "kiwi": Kiwi,
        "manzana": Manzana,
        "papa": Papa,
        "zanahoria": Zanahoria
    }

    def __init__(self, detector_alimentos: DetectorAlimento):
        if not isinstance(detector_alimentos, DetectorAlimento):
            raise TypeError("Se necesita una instancia de DetectorAlimento.")
        self.__detector = detector_alimentos
        self.__ultimo_cajon_procesado: Optional[Cajon] = None

    def _crear_objeto_alimento(self, info_detectada: Dict[str, Any]) -> Optional[Alimento]:
        """Método interno para crear instancias de Alimento a partir de datos del detector."""
        nombre_bruto = info_detectada.get("alimento")
        peso_bruto = info_detectada.get("peso")

        if not isinstance(nombre_bruto, str) or not isinstance(peso_bruto, (int, float)):
            
            return None

        nombre_limpio = nombre_bruto.lower()

        if nombre_limpio == "undefined":
            return None

        ClaseAlimento = self._MAPA_CLASES_ALIMENTO.get(nombre_limpio)
        if ClaseAlimento:
            try:
                return ClaseAlimento(peso_kg=float(peso_bruto))
            except ValueError as e:
                return None
        return None

    def procesar_nuevo_cajon(self, num_alimentos_objetivo: int) -> Cajon:
        if not isinstance(num_alimentos_objetivo, int) or num_alimentos_objetivo <= 0:
            num_alimentos_objetivo = 10

        cajon_actual = Cajon(capacidad_maxima=num_alimentos_objetivo)
        alimentos_validos_cargados = 0
        intentos_deteccion_total = 0
        max_intentos_global = num_alimentos_objetivo * 7


        while alimentos_validos_cargados < num_alimentos_objetivo and intentos_deteccion_total < max_intentos_global:
            intentos_deteccion_total += 1
            info_detectada = self.__detector.detectar_alimento()
            alimento_obj = self._crear_objeto_alimento(info_detectada)  # Cambio aquí

            if alimento_obj and cajon_actual.agregar_alimento(alimento_obj):
                alimentos_validos_cargados += 1

        if alimentos_validos_cargados < num_alimentos_objetivo:
            
            pass

        cajon_actual.calcular_metricas()
        self.__ultimo_cajon_procesado = cajon_actual
       
        return cajon_actual

    def get_ultimo_cajon_procesado(self) -> Optional[Cajon]:
        return self.__ultimo_cajon_procesado
