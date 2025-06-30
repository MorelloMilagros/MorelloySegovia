from datetime import datetime
from flask import render_template
from modules.reporte_base import ReporteBase
from xhtml2pdf import pisa
from io import BytesIO
class ReporteHTML(ReporteBase):
    """
    Estrategia concreta para generar el reporte en formato HTML.
    """
    def generar(self, departamento: str) -> str:
        """
        Genera el reporte renderizando una plantilla de Flask.

        Returns:
            str: Una cadena de texto con el contenido HTML del reporte.
        """
        reclamos, stats = self._obtener_datos(departamento)
        
        html_renderizado = render_template(
            'reporte.html',
            lista_reclamos=reclamos,
            stats=stats,
            departamento=departamento,
            fecha_generacion=datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        )
        return html_renderizado
    


class ReportePDF(ReporteBase):
    """
    Estrategia concreta para generar el reporte en formato PDF.
    """
    def generar(self, departamento: str) -> bytes:
        """
        Genera el reporte, lo renderiza como HTML y lo convierte a PDF.

        Returns:
            bytes: El contenido del archivo PDF en bytes.
        """
        reclamos, stats = self._obtener_datos(departamento)

        html_renderizado = render_template(
            'reporte.html',
            lista_reclamos=reclamos,
            stats=stats,
            departamento=departamento,
            fecha_generacion=datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
            is_pdf=True  # Flag para la plantilla, por si necesita URLs absolutas para las imágenes
        )

        pdf_buffer = BytesIO()
        pisa_status = pisa.CreatePDF(
            BytesIO(html_renderizado.encode('UTF-8')),
            dest=pdf_buffer
        )

        if pisa_status.err:
            raise Exception(f"Error al generar el PDF: {pisa_status.err}")

        pdf_buffer.seek(0)
        return pdf_buffer.read()