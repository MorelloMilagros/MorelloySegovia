from abc import ABC, abstractmethod

class ReporteAbstracto(ABC):

    @abstractmethod
    def obtener_reporte(self, algo):
        pass

    @abstractmethod
    def comparar_reportes(self, reporte):
        pass

    @abstractmethod
    def generar_reporte (self, entidad):
        pass

    



