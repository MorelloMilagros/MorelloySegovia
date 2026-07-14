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
    
    def obtener_datos_dashboard(self, departamento: str = None) -> tuple:
        """
        Obtiene los datos necesarios para el dashboard.
        Si se especifica un 'departamento', filtra por él.
        Si 'departamento' es None, obtiene TODOS los reclamos.
        """
        if departamento:
            # Flujo normal para un jefe de departamento
            lista_reclamos = self._gestor_reclamos.listar_reclamos_por_departamento(departamento)
        else:
            # Flujo para el secretario: obtener todos los reclamos
            lista_reclamos = self._gestor_reclamos.obtener_todos_los_reclamos()

        # Usamos una instancia de Reporte para acceder a la lógica de cálculo
        # que ya tenemos, pasándole la lista de reclamos (filtrada o completa).
        reporte_temp = ReporteHTML(self._gestor_reclamos, self._graficador)
        stats = reporte_temp._calcular_estadisticas(lista_reclamos)
        
        return lista_reclamos, stats
    
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
    
    def obtener_imagen_grafico(self, tipo_grafico: str, departamento: str) -> bytes:
        """
        Genera y devuelve la imagen de un gráfico específico en bytes.
 
        Args:
            tipo_grafico (str): El tipo de gráfico a generar ('torta' o 'nube').
            departamento (str): El departamento por el cual filtrar los datos.
 
        Returns:
            bytes: La imagen del gráfico en formato PNG, o None si no hay datos.
 
        Raises:
            ValueError: Si el tipo de gráfico no es válido.
        """
        lista_reclamos = self._gestor_reclamos.listar_reclamos_por_departamento(departamento)
        reporte_temp = ReporteHTML(self._gestor_reclamos, self._graficador)
        stats = reporte_temp._calcular_estadisticas(lista_reclamos)
 
        if tipo_grafico == 'torta':
            datos_torta = {
                'Pendientes': stats['pendientes'],
                'En proceso': stats['en_proceso'],
                'Resueltos': stats['resueltos'],
                'Inválidos': stats['invalidos'],
            }
            return self._graficador.crear_grafico_torta(datos_torta, f'Reclamos - {departamento}')
        elif tipo_grafico == 'nube':
            return self._graficador.crear_nube_palabras(stats['palabras_clave'], f'Palabras clave - {departamento}')
        else:
            raise ValueError(f"Tipo de gráfico '{tipo_grafico}' no válido. Use 'torta' o 'nube'.")