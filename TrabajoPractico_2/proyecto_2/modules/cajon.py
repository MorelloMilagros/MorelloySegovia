# modules/cajon.py
from typing import List, Dict, Optional, Iterable
from modules.alimento import Alimento

class Cajon:
    """Representa un cajón de alimentos y calcula sus métricas."""
    ALIMENTOS_CONOCIDOS = ["Kiwi", "Manzana", "Papa", "Zanahoria"]
    TIPOS_CONOCIDOS = ["Fruta", "Verdura"]

    def __init__(self, capacidad_maxima: int):
        if not isinstance(capacidad_maxima, int) or capacidad_maxima <= 0:
            raise ValueError("La capacidad máxima del cajón debe ser un entero positivo.")
        self.__capacidad_maxima: int = capacidad_maxima
        self.__alimentos_en_cajon: List[Alimento] = []
        self.__peso_total_kg: float = 0.0
        self.__aw_prom_por_alimento: Dict[str, float] = {n: 0.0 for n in self.ALIMENTOS_CONOCIDOS}
        self.__aw_prom_por_tipo: Dict[str, float] = {t: 0.0 for t in self.TIPOS_CONOCIDOS}
        self.__aw_prom_total_cajon: float = 0.0
        self.__advertencia: str = "Cajón no procesado o vacío."

    # ... (Properties sin cambios) ...
    @property
    def capacidad_maxima(self):
        return self.__capacidad_maxima
        
    @property
    def alimentos_en_cajon(self):
        return self.__alimentos_en_cajon
        
    @property
    def peso_total_kg(self):
        return self.__peso_total_kg
        
    @peso_total_kg.setter
    def peso_total_kg(self, value):
        self.__peso_total_kg = value
        
    @property
    def aw_prom_por_alimento(self):
        return self.__aw_prom_por_alimento
        
    @aw_prom_por_alimento.setter
    def aw_prom_por_alimento(self, value):
        self.__aw_prom_por_alimento = value
        
    @property
    def aw_prom_por_tipo(self):
        return self.__aw_prom_por_tipo
        
    @aw_prom_por_tipo.setter
    def aw_prom_por_tipo(self, value):
        self.__aw_prom_por_tipo = value
        
    @property
    def aw_prom_total_cajon(self):
        return self.__aw_prom_total_cajon
        
    @aw_prom_total_cajon.setter
    def aw_prom_total_cajon(self, value):
        self.__aw_prom_total_cajon = value
        
    @property
    def advertencia(self):
        return self.__advertencia
        
    @advertencia.setter
    def advertencia(self, value):
        self.__advertencia = value

    def _inicializar_metricas(self):
        """Resetea las métricas del cajón a sus valores por defecto."""
        self.__peso_total_kg = 0.0
        self.__aw_prom_por_alimento = {n: 0.0 for n in self.ALIMENTOS_CONOCIDOS}
        self.__aw_prom_por_tipo = {t: 0.0 for t in self.TIPOS_CONOCIDOS}
        self.__aw_prom_total_cajon = 0.0
        self.__advertencia = "Cajón no procesado o vacío."

    def agregar_alimento(self, alimento: Alimento) -> bool:
        """Agrega un alimento al cajón si no está lleno."""
        if not self.esta_lleno():
            self.__alimentos_en_cajon.append(alimento)
            return True
        return False

    def esta_lleno(self) -> bool:
        """Verifica si el cajón ha alcanzado su capacidad máxima."""
        return len(self.__alimentos_en_cajon) >= self.__capacidad_maxima

    def get_num_alimentos(self) -> int:
        """Obtiene el número actual de alimentos en el cajón."""
        return len(self.__alimentos_en_cajon)

    def calcular_metricas(self) -> None:
        """Calcula todas las métricas del cajón."""
        # print("\n--- INICIO CALCULAR METRICAS ---") # ELIMINADO
        self._inicializar_metricas()
        num_alimentos_actual = self.get_num_alimentos()
        # print(f"Número de alimentos en el cajón: {num_alimentos_actual}") # ELIMINADO

        if num_alimentos_actual == 0:
            self.__advertencia = "Cajón vacío. No se pueden calcular métricas."
            # print(f"Advertencia: {self.__advertencia}") # ELIMINADO
            return

        self.peso_total_kg = sum(al.peso_kg for al in self.__alimentos_en_cajon)
        # print(f"Peso total del cajón: {self.peso_total_kg:.3f} kg") # ELIMINADO

        sumas_aw_alimento = {n: 0.0 for n in self.ALIMENTOS_CONOCIDOS}
        conteos_alimento = {n: 0 for n in self.ALIMENTOS_CONOCIDOS}
        sumas_aw_tipo = {t: 0.0 for t in self.TIPOS_CONOCIDOS}
        conteos_tipo = {t: 0 for t in self.TIPOS_CONOCIDOS}
        suma_aw_total_cajon = 0.0

        # print("\n--- Iterando sobre los alimentos en el cajón ---") # ELIMINADO
        for al in self.__alimentos_en_cajon:
            aw_actual = al.calcular_aw()
            # print(f"   - Alimento: {al.nombre}, Tipo: {al.tipo_alimento}, AW: {aw_actual:.3f}") # ELIMINADO
            suma_aw_total_cajon += aw_actual
            if al.nombre in self.ALIMENTOS_CONOCIDOS:
                sumas_aw_alimento[al.nombre] += aw_actual
                conteos_alimento[al.nombre] += 1
            if al.tipo_alimento in self.TIPOS_CONOCIDOS:
                sumas_aw_tipo[al.tipo_alimento] += aw_actual
                conteos_tipo[al.tipo_alimento] += 1

        aw_prom_por_alimento_calculado = {} # Renombrado para evitar confusión con la property
        # print("\n--- Sumas y conteos por alimento ---") # ELIMINADO
        for nombre_alimento in self.ALIMENTOS_CONOCIDOS: # Renombrado para claridad
            # print(f"   - {nombre_alimento}: Suma AW = {sumas_aw_alimento[nombre_alimento]:.3f}, Conteo = {conteos_alimento[nombre_alimento]}") # ELIMINADO
            aw_prom_por_alimento_calculado[nombre_alimento] = (sumas_aw_alimento[nombre_alimento] / conteos_alimento[nombre_alimento]) if conteos_alimento[nombre_alimento] > 0 else 0.0
            # print(f"     -> AW Promedio = {aw_prom_por_alimento_calculado[nombre_alimento]:.3f}") # ELIMINADO
        self.aw_prom_por_alimento = aw_prom_por_alimento_calculado

        aw_prom_por_tipo_calculado = {} # Renombrado para evitar confusión con la property
        # print("\n--- Sumas y conteos por tipo ---") # ELIMINADO
        for tipo_alimento in self.TIPOS_CONOCIDOS: # Renombrado para claridad
            # print(f"   - {tipo_alimento}: Suma AW = {sumas_aw_tipo[tipo_alimento]:.3f}, Conteo = {conteos_tipo[tipo_alimento]}") # ELIMINADO
            aw_prom_por_tipo_calculado[tipo_alimento] = (sumas_aw_tipo[tipo_alimento] / conteos_tipo[tipo_alimento]) if conteos_tipo[tipo_alimento] > 0 else 0.0
            # print(f"     -> AW Promedio = {aw_prom_por_tipo_calculado[tipo_alimento]:.3f}") # ELIMINADO
        self.aw_prom_por_tipo = aw_prom_por_tipo_calculado

        self.aw_prom_total_cajon = suma_aw_total_cajon / num_alimentos_actual
        # print(f"\nAW Promedio Total del Cajón: {self.aw_prom_total_cajon:.3f}") # ELIMINADO

        epsilon = 1e-9
        mensajes_adv = []
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

        # print(f"Advertencia final: {self.advertencia}") # ELIMINADO
        # print("--- FIN CALCULAR METRICAS ---\n") # ELIMINADO

    def __iter__(self):
        return iter(self.__alimentos_en_cajon)

    def __str__(self) -> str:
        # El método __str__ usualmente se mantiene con prints o estructura de string para la depuración
        # o representación del objeto. Si deseas eliminar prints indirectos de aquí,
        # deberías modificar este método para que solo retorne la data cruda o nada.
        # Por ahora, lo mantendré como está, ya que su propósito es generar una representación en string.
        info = [
            f"--- ESTADO DEL CAJÓN ({self.get_num_alimentos()}/{self.capacidad_maxima} alimentos) ---",
            f"Peso Total: {self.peso_total_kg:.2f} kg",
            f"AW Promedio Total del Cajón: {self.aw_prom_total_cajon:.3f}",
            "AW Promedios por Tipo:",
            f"  Frutas: {self.aw_prom_por_tipo.get('Fruta', 0.0):.3f}", # Usar .get por si acaso
            f"  Verduras: {self.aw_prom_por_tipo.get('Verdura', 0.0):.3f}",
            "AW Promedios por Alimento Específico:"
        ]
        for nombre, aw_prom in self.aw_prom_por_alimento.items():
            info.append(f"  {nombre}: {aw_prom:.3f}")
        info.append(f"Advertencia: {self.advertencia}")
        if self.get_num_alimentos() > 0:
            info.append("Contenido Detallado:")
            for al in self.__alimentos_en_cajon:
                info.append(f"  - {str(al)}") # str(al) llama al __str__ de Alimento
        else:
            info.append("El cajón está vacío.")
        return "\n".join(info)