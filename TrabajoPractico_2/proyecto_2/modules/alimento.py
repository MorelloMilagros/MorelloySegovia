from abc import ABC, abstractmethod
import math

class Alimento(ABC):
    """Clase base abstracta para un alimento con nombre, peso y cálculo de aw.H"""
    def __init__(self, nombre: str, peso_kg: float):
        if not isinstance(peso_kg, (int, float)) or peso_kg <= 0:
            raise ValueError(f"El peso para '{nombre}' debe ser un número positivo, se recibió {peso_kg}.")
        self._nombre: str = nombre
        self._peso_kg: float = round(peso_kg, 3)
        self._tipo_alimento: str = ""

# Propiedades para acceso controlado
    @property
    def nombre(self):
        return self._nombre
        
    @property
    def peso_kg(self):
        return self._peso_kg
        
    @property
    def tipo_alimento(self):
        return self._tipo_alimento

    @abstractmethod # <-- DEFINE EL CONTRATO
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
        self._tipo_alimento = "Fruta"


class Verdura(Alimento):
    """Clase base para alimentos de tipo Verdura."""
    def __init__(self, nombre: str, peso_kg: float):
        super().__init__(nombre, peso_kg)
        self._tipo_alimento = "Verdura" 


# --- Clases específicas ---
class Kiwi(Fruta):
    def __init__(self, peso_kg: float):
        super().__init__('Kiwi', peso_kg)  

    def calcular_aw(self) -> float: # <-- CUMPLE EL CONTRATO
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