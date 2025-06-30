from abc import ABC, abstractmethod
from typing import Union

class Reporte(ABC):
    """
    Define la interfaz para una estrategia de generación de reportes.
    Cualquier clase que genere un reporte en un formato específico debe
    implementar esta interfaz.
    """

    @abstractmethod
    def generar(self, departamento: str) -> Union[str, bytes]:
        """
        Genera el reporte completo en su formato específico.

        Args:
            departamento (str): El departamento para el cual se genera el reporte.

        Returns:
            Union[str, bytes]: El contenido del reporte, ya sea como una cadena
                               de texto (para HTML) o como bytes (para PDF).
        """
        raise NotImplementedError
    



