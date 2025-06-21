from modules.reporte_abstracto import Reporte
from modules.gestor_reclamos import GestorDeReclamos

class Analitica:
    """
    Clase fachada (Facade) que simplifica el acceso al subsistema de reportes y
    visualizaciones. Es el único punto de entrada que el controlador (server.py)
    necesita para obtener datos analíticos.
    """
    def __init__(self, generador_reportes: Reporte, gestor_reclamos: GestorDeReclamos):
        """
        Inicializa la fachada con las dependencias necesarias.
        
        Args:
            generador_reportes (Reporte): La implementación concreta para generar reportes.
            gestor_reclamos (GestorDeReclamos): El gestor para obtener listas de reclamos.
        """
        self.__generador_reportes = generador_reportes
        self.__gestor_reclamos = gestor_reclamos

    def obtener_datos_dashboard(self, departamento: str) -> tuple:
        """
        Obtiene todos los datos necesarios para el dashboard principal.
        
        Returns:
            tuple: Una tupla conteniendo (lista_de_reclamos, estadisticas).
        """
        reclamos = self.__gestor_reclamos.listar_reclamos_por_departamento(departamento)
        stats = self.__generador_reportes.generar_reporte(departamento=departamento)
        return reclamos, stats
    
    def obtener_datos_reporte_completo(self, departamento: str) -> tuple:
        """
        Obtiene todos los datos necesarios para la página de analítica o el PDF.
        """
        return self.obtener_datos_dashboard(departamento)

    def obtener_imagen_grafico(self, tipo_grafico: str, departamento: str) -> bytes:
        """
        Solicita la generación de una imagen de un gráfico específico.
        
        Args:
            tipo_grafico (str): 'barras', 'torta', o 'nube'.
            departamento (str): El departamento para el cual generar el gráfico.
            
        Returns:
            bytes: La imagen del gráfico.
        """
        return self.__generador_reportes.generar_visualizacion(tipo_grafico, departamento=departamento)
