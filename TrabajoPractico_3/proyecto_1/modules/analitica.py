from modules.gestor_reclamos import GestorDeReclamos
from modules.gestor_reclamos import GestorDeReclamos
from modules.graficador_abstracto import Graficador
from modules.reporte_concreto import ReporteHTML,ReportePDF

class Analitica:
    """
    Clase fachada (Facade) que actúa como un punto de entrada simplificado
    para el subsistema de reportes y analítica.
    """
    def __init__(self, gestor_reclamos: GestorDeReclamos, graficador: Graficador):
        self._gestor_reclamos = gestor_reclamos
        self._graficador = graficador

    def obtener_datos_dashboard(self, departamento: str) -> tuple:
        """
        Obtiene los datos necesarios para el dashboard.
        """
        # Usamos una de las estrategias para acceder al método compartido _obtener_datos
        reporte_temp = ReporteHTML(self._gestor_reclamos, self._graficador)
        return reporte_temp._obtener_datos(departamento)
    
    def generar_reporte_formateado(self, departamento: str, formato: str) -> tuple:
        """
        Selecciona la estrategia de reporte correcta, la ejecuta y devuelve
        el resultado listo para ser enviado como una respuesta HTTP.
        """
        if formato == 'pdf':
            estrategia = ReportePDF(self._gestor_reclamos, self._graficador)
            mimetype = 'application/pdf'
            headers = {'Content-Disposition': f'attachment;filename=reporte_{departamento}.pdf'}
        elif formato == 'html':
            estrategia = ReporteHTML(self._gestor_reclamos, self._graficador)
            mimetype = 'text/html'
            headers = {}
        else:
            raise ValueError(f"Formato '{formato}' no soportado.")
        
        output = estrategia.generar(departamento)
        
        return (output, mimetype, headers)
