from abc import ABC, abstractmethod

class Graficador(ABC):

    @abstractmethod
    def crear_grafico_barras(self, datos: dict, titulo:str, etiqueta_x:str, etiqueta_y:str)-> bytes:
        """
        Crea un gráfico de barras.

        Args:
            datos (dict): Diccionario con las etiquetas y valores.
            titulo (str): Título del gráfico.
            etiqueta_x (str): Etiqueta del eje X.
            etiqueta_y (str): Etiqueta del eje Y.

        Returns:
            bytes: La imagen del gráfico en formato de bytes.
        """
        raise NotImplementedError("Debe implementar el método 'crear_grafica_barras'")
    
    @abstractmethod
    def crear_grafico_torta(self, datos: dict, titulo: str) -> bytes:
        """
        Crea un gráfico de torta.

        Args:
            datos (dict): Diccionario con las etiquetas y valores para las porciones.
            titulo (str): Título del gráfico.

        Returns:
            bytes: La imagen del gráfico en formato de bytes. Puede devolver None si no hay datos.
        """
        raise NotImplementedError("Debe implementar el método 'crear_grafico_torta'")
    
    @abstractmethod
    def crear_nube_palabras(self, palabras_frecuentes: list, titulo: str) -> bytes:
        """
        Crea una nube de palabras.

        Args:
            palabras_frecuentes (list): Lista de tuplas (palabra, frecuencia).
            titulo (str): Título del gráfico.

        Returns:
            bytes: La imagen del gráfico en formato de bytes. Puede devolver None si no hay datos.
        """
        raise NotImplementedError
