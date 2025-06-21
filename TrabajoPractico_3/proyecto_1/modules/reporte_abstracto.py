from abc import ABC, abstractmethod

class Reporte(ABC):

    @abstractmethod
    def generar_reporte (self, **kwars):
        """
        Método abstracto para generar un reporte.
        Cada implementación concreta definirá cómo se generan los datos
        y qué formato tienen.

        Args:
            **kwargs: Argumentos de palabra clave que pueden ser necesarios
                      para generar el reporte, como 'departamento', 'fecha_inicio', etc.

        Returns:
            dict: Un diccionario con los datos del reporte.
        """
        raise NotImplementedError("Debe implementar el método 'generar_reporte'")
    
    @abstractmethod
    def generar_visualizacion(self, tipo_grafico: str, **kwargs):
        """
        Método abstracto para generar una visualización específica (gráfico).

        Args:
            tipo_grafico (str): El tipo de gráfico a generar (ej: 'barras', 'torta').
            **kwargs: Argumentos necesarios para la visualización.

        Returns:
            bytes: La imagen del gráfico en formato de bytes, lista para ser servida.
        """
        raise NotImplementedError


