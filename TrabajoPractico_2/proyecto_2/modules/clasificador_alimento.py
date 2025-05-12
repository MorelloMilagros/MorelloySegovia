import math
from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Type # Uso de Type para el mapa

# Importar DetectorAlimento solo para type hinting en ControlCinta,
# la instancia se inyecta.
from .detector_alimento import DetectorAlimento


# --- Definición de Clases de Alimentos ---
# --- Clase base abstracta ---
class Alimento(ABC):
    """Clase base abstracta para un alimento con nombre, peso y cálculo de aw."""
    def __init__(self, nombre: str, peso_kg: float):
        if not isinstance(peso_kg, (int, float)) or peso_kg <= 0:
            raise ValueError(f"El peso para '{nombre}' debe ser un número positivo, se recibió {peso_kg}.")
        self.nombre: str = nombre
        self.peso_kg: float = round(peso_kg, 3)
        self.tipo_alimento: str = ""

    @abstractmethod
    def calcular_aw(self) -> float:
        """Calcula y retorna la actividad acuosa (aw) del alimento."""
        pass

    def _limitar_aw(self, aw_calculada: float) -> float:
        """Asegura que el valor de aw esté entre 0.0 y 1.0, redondeado a 3 decimales."""
        return round(max(0.0, min(1.0, aw_calculada)), 3)

    def __str__(self) -> str:
        return (f"{self.nombre} ({self.tipo_alimento}) - "
                f"Peso: {self.peso_kg:.3f} kg, AW: {self.calcular_aw():.3f}")


# --- Clases intermedias ---
class Fruta(Alimento):
    """Clase base para alimentos de tipo Fruta."""
    def __init__(self, nombre: str, peso_kg: float):
        super().__init__(nombre, peso_kg)
        self.tipo_alimento = "Fruta"


class Verdura(Alimento):
    """Clase base para alimentos de tipo Verdura."""
    def __init__(self, nombre: str, peso_kg: float):
        super().__init__(nombre, peso_kg)
        self.tipo_alimento = "Verdura"


# --- Clases específicas ---
class Kiwi(Fruta):
    def __init__(self, peso_kg: float):
        super().__init__('Kiwi', peso_kg)  

    def calcular_aw(self) -> float:
        if self.peso_kg >= 0.6: 
            return 1.0
        C = 18
        term = C * self.peso_kg
        numerador = 1 - math.exp(-term)
        denominador = 1 + math.exp(-term)
        aw = 0.96 * (numerador / denominador)
        return self._limitar_aw(aw)


class Manzana(Fruta):
    def __init__(self, peso_kg: float):
        super().__init__("Manzana", peso_kg)

    def calcular_aw(self) -> float:
        if self.peso_kg >= 0.6:
            return 1.0
        C = 15
        m = self.peso_kg
        termino = (C * m) ** 2
        aw = 0.97 * (termino / (1 + termino))
        return self._limitar_aw(aw)


class Papa(Verdura):
    def __init__(self, peso_kg: float):
        super().__init__("Papa", peso_kg)

    def calcular_aw(self) -> float:
        if self.peso_kg >= 0.6:
            return 1.0
        C = 18
        m = self.peso_kg
        aw = 0.66 * math.atan(C * m)
        return self._limitar_aw(aw)


class Zanahoria(Verdura):
    def __init__(self, peso_kg: float):
        super().__init__("Zanahoria", peso_kg)

    def calcular_aw(self) -> float:
        if self.peso_kg >= 0.6:
            return 1.0
        C = 10
        m = self.peso_kg
        aw = 0.96 * (1 - math.exp(-C * m))
        return self._limitar_aw(aw)

# --- Clase Cajón ---
class Cajon:
    """Representa un cajón de alimentos y calcula sus métricas."""
    ALIMENTOS_CONOCIDOS = ["Kiwi", "Manzana", "Papa", "Zanahoria"]
    TIPOS_CONOCIDOS = ["Fruta", "Verdura"]

    def __init__(self, capacidad_maxima: int):
        if not isinstance(capacidad_maxima, int) or capacidad_maxima <= 0:
            raise ValueError("La capacidad máxima del cajón debe ser un entero positivo.")
        self.capacidad_maxima: int = capacidad_maxima
        self.alimentos_en_cajon: List[Alimento] = []
        self._inicializar_metricas()

    def _inicializar_metricas(self):
        """Resetea las métricas del cajón a sus valores por defecto."""
        self.peso_total_kg: float = 0.0
        self.aw_prom_por_alimento: Dict[str, float] = {n: 0.0 for n in self.ALIMENTOS_CONOCIDOS}
        self.aw_prom_por_tipo: Dict[str, float] = {t: 0.0 for t in self.TIPOS_CONOCIDOS}
        self.aw_prom_total_cajon: float = 0.0
        self.advertencia: str = "Cajón no procesado o vacío."

    def agregar_alimento(self, alimento: Alimento) -> bool:
        if not self.esta_lleno():
            self.alimentos_en_cajon.append(alimento)
            return True
        return False

    def esta_lleno(self) -> bool:
        return len(self.alimentos_en_cajon) >= self.capacidad_maxima

    def get_num_alimentos(self) -> int:
        return len(self.alimentos_en_cajon)

    def calcular_metricas(self) -> None:
        print("\n--- INICIO CALCULAR METRICAS ---")
        self._inicializar_metricas() # Resetear antes de calcular
        num_alimentos_actual = self.get_num_alimentos()
        print(f"Número de alimentos en el cajón: {num_alimentos_actual}")

        if num_alimentos_actual == 0:
            self.advertencia = "Cajón vacío. No se pueden calcular métricas."
            print(f"Advertencia: {self.advertencia}")
            return

        self.peso_total_kg = sum(al.peso_kg for al in self.alimentos_en_cajon)
        print(f"Peso total del cajón: {self.peso_total_kg:.3f} kg")

        sumas_aw_alimento: Dict[str, float] = {n: 0.0 for n in self.ALIMENTOS_CONOCIDOS}
        conteos_alimento: Dict[str, int] = {n: 0 for n in self.ALIMENTOS_CONOCIDOS}
        sumas_aw_tipo: Dict[str, float] = {t: 0.0 for t in self.TIPOS_CONOCIDOS}
        conteos_tipo: Dict[str, int] = {t: 0 for t in self.TIPOS_CONOCIDOS}
        suma_aw_total_cajon: float = 0.0

        print("\n--- Iterando sobre los alimentos en el cajón ---")
        for al in self.alimentos_en_cajon:
            aw_actual = al.calcular_aw()
            print(f"  - Alimento: {al.nombre}, Tipo: {al.tipo_alimento}, AW: {aw_actual:.3f}")
            suma_aw_total_cajon += aw_actual
            if al.nombre in self.ALIMENTOS_CONOCIDOS:
                sumas_aw_alimento[al.nombre] += aw_actual
                conteos_alimento[al.nombre] += 1
            if al.tipo_alimento in self.TIPOS_CONOCIDOS:
                sumas_aw_tipo[al.tipo_alimento] += aw_actual
                conteos_tipo[al.tipo_alimento] += 1

        print("\n--- Sumas y conteos por alimento ---")
        for nombre in self.ALIMENTOS_CONOCIDOS:
            print(f"  - {nombre}: Suma AW = {sumas_aw_alimento[nombre]:.3f}, Conteo = {conteos_alimento[nombre]}")
            self.aw_prom_por_alimento[nombre] = (sumas_aw_alimento[nombre] / conteos_alimento[nombre]) \
                                               if conteos_alimento[nombre] > 0 else 0.0
            print(f"    -> AW Promedio = {self.aw_prom_por_alimento[nombre]:.3f}")

        print("\n--- Sumas y conteos por tipo ---")
        for tipo in self.TIPOS_CONOCIDOS:
            print(f"  - {tipo}: Suma AW = {sumas_aw_tipo[tipo]:.3f}, Conteo = {conteos_tipo[tipo]}")
            self.aw_prom_por_tipo[tipo] = (sumas_aw_tipo[tipo] / conteos_tipo[tipo]) \
                                          if conteos_tipo[tipo] > 0 else 0.0
            print(f"    -> AW Promedio = {self.aw_prom_por_tipo[tipo]:.3f}")

        self.aw_prom_total_cajon = suma_aw_total_cajon / num_alimentos_actual
        print(f"\nAW Promedio Total del Cajón: {self.aw_prom_total_cajon:.3f}")

        epsilon = 1e-9
        mensajes_adv: List[str] = []
        for nombre, aw_prom in self.aw_prom_por_alimento.items():
            if aw_prom > (0.90 + epsilon):
                mensajes_adv.append(f"AW Promedio {nombre} ({aw_prom:.3f}) > 0.90")
        for tipo, aw_prom in self.aw_prom_por_tipo.items():
            if aw_prom > (0.90 + epsilon):
                mensajes_adv.append(f"AW Promedio {tipo} ({aw_prom:.3f}) > 0.90")
        if self.aw_prom_total_cajon > (0.90 + epsilon):
            mensajes_adv.append(f"AW Promedio Total del Cajón ({self.aw_prom_total_cajon:.3f}) > 0.90")

        if mensajes_adv:
            self.advertencia = "¡ADVERTENCIA! " + "; ".join(mensajes_adv) + ". Se recomienda inspeccionar el cajón."
        else:
            self.advertencia = "Todos los promedios de actividad acuosa están dentro de los límites aceptables."

        print(f"Advertencia final: {self.advertencia}")
        print("--- FIN CALCULAR METRICAS ---\n")

    def __iter__(self):
        return iter(self.alimentos_en_cajon)

    def __str__(self) -> str:
        info = [
            f"--- ESTADO DEL CAJÓN ({self.get_num_alimentos()}/{self.capacidad_maxima} alimentos) ---",
            f"Peso Total: {self.peso_total_kg:.2f} kg",
            f"AW Promedio Total del Cajón: {self.aw_prom_total_cajon:.3f}",
            "AW Promedios por Tipo:",
            f"  Frutas: {self.aw_prom_por_tipo['Fruta']:.3f}",
            f"  Verduras: {self.aw_prom_por_tipo['Verdura']:.3f}",
            "AW Promedios por Alimento Específico:"
        ]
        for nombre, aw_prom in self.aw_prom_por_alimento.items():
            info.append(f"  {nombre}: {aw_prom:.3f}")
        info.append(f"Advertencia: {self.advertencia}")
        if self.alimentos_en_cajon:
            info.append("Contenido Detallado:")
            for al in self.alimentos_en_cajon:
                info.append(f"  - {al}")
        else:
            info.append("El cajón está vacío.")
        return "\n".join(info)


# --- Fábrica de Objetos Alimento ---
_MAPA_CLASES_ALIMENTO: Dict[str, Type[Alimento]] = {
    "kiwi": Kiwi,
    "manzana": Manzana,
    "papa": Papa,
    "zanahoria": Zanahoria
}

def crear_objeto_alimento(info_detectada: Dict[str, any]) -> Optional[Alimento]:
    """Crea una instancia de Alimento a partir de la info del detector."""
    nombre_bruto = info_detectada.get("alimento")
    peso_bruto = info_detectada.get("peso")

    if not isinstance(nombre_bruto, str) or not isinstance(peso_bruto, (int, float)):
        print(f"[CrearObj] Error: Datos de entrada inválidos: {info_detectada}")
        return None

    nombre_limpio = nombre_bruto.lower()

    if nombre_limpio == "undefined": # AJUSTADO: "undefined" del detector del profesor
        return None

    ClaseAlimento = _MAPA_CLASES_ALIMENTO.get(nombre_limpio)
    if ClaseAlimento:
        try:
            return ClaseAlimento(peso_kg=float(peso_bruto))
        except ValueError as e:
            print(f"[CrearObj] Error al instanciar {nombre_limpio} con peso {peso_bruto}: {e}")
            return None
    else:
        # print(f"[CrearObj] Alimento desconocido: '{nombre_limpio}'")
        return None

# --- Clase de Control de la Cinta Transportadora ---
class ControlCinta:
    """Orquesta el llenado de cajones con alimentos detectados."""
    def __init__(self, detector_alimentos: DetectorAlimento):
        if not isinstance(detector_alimentos, DetectorAlimento):
            raise TypeError("Se necesita una instancia de DetectorAlimento.")
        self.detector = detector_alimentos
        self._ultimo_cajon_procesado: Optional[Cajon] = None

    def procesar_nuevo_cajon(self, num_alimentos_objetivo: int) -> Cajon:
        if not isinstance(num_alimentos_objetivo, int) or num_alimentos_objetivo <= 0:
            print(f"[ControlCinta] N objetivo inválido ({num_alimentos_objetivo}). Usando default de 10.")
            num_alimentos_objetivo = 10

        cajon_actual = Cajon(capacidad_maxima=num_alimentos_objetivo)
        alimentos_validos_cargados = 0
        intentos_deteccion_total = 0
        max_intentos_global = num_alimentos_objetivo * 7 # Límite más generoso

        print(f"[ControlCinta] Iniciando cajón. Objetivo: {num_alimentos_objetivo} alimentos válidos.")

        while alimentos_validos_cargados < num_alimentos_objetivo and intentos_deteccion_total < max_intentos_global:
            intentos_deteccion_total += 1
            info_detectada = self.detector.detectar_alimento()
            alimento_obj = crear_objeto_alimento(info_detectada)

            if alimento_obj:
                if cajon_actual.agregar_alimento(alimento_obj):
                    alimentos_validos_cargados += 1
                    # print(f"  [CC] Agregado ({alimentos_validos_cargados}/{num_alimentos_objetivo}): {alimento_obj.nombre}")
            # else: # Alimento "undefined" o no reconocido, se descarta.
                # print(f"  [CC] Descartado: {info_detectada.get('alimento')} (Intento {intentos_deteccion_total})")

        if alimentos_validos_cargados < num_alimentos_objetivo:
            print(f"ADVERTENCIA [ControlCinta]: Cajón no llenado al objetivo. "
                  f"Cargados: {alimentos_validos_cargados}/{num_alimentos_objetivo} tras {intentos_deteccion_total} detecciones.")
        else:
            print(f"[ControlCinta] Cajón llenado con {alimentos_validos_cargados} alimentos.")

        cajon_actual.calcular_metricas()
        self._ultimo_cajon_procesado = cajon_actual
        print(f"[ControlCinta] Métricas calculadas. {cajon_actual.advertencia.split('.')[0]}.") # Solo primera parte advertencia
        return cajon_actual

    def get_ultimo_cajon_procesado(self) -> Optional[Cajon]:
        return self._ultimo_cajon_procesado

# (El bloque __main__ de este archivo puede permanecer como en la versión anterior para pruebas directas)
if __name__ == "__main__":
    print("\nEjecutando pruebas internas de clasificador_alimento.py...")
    # ... (mismas pruebas que antes para Alimento, Cajon, ControlCinta, si se desean)
    # Prueba de ControlCinta
    print("\n--- Prueba de ControlCinta ---")
    # Para probar ControlCinta, necesitamos una instancia de DetectorAlimento
    # La siembra debe hacerse ANTES de crear el detector, ya que el __init__ del profesor no toma seed
    random.seed(101) 
    np.random.seed(101)
    detector_para_control = DetectorAlimento() 
    control = ControlCinta(detector_alimentos=detector_para_control)
    
    N_objetivo = 3
    print(f"Procesando un cajón con ControlCinta (N={N_objetivo})...")
    cajon_procesado_main = control.procesar_nuevo_cajon(num_alimentos_objetivo=N_objetivo)
    print("\nResultado del cajón procesado por ControlCinta (main):")
    print(cajon_procesado_main)
