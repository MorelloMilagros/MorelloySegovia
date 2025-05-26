import os
from PyPDF4 import PdfFileMerger
from flask import send_file
import os
# Obtiene el directorio raíz del proyecto 
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Define correctamente las rutas dentro de "static/"
STATIC_DIR = os.path.join(BASE_DIR, "static")
PDF_DIR = os.path.join(STATIC_DIR, "pdf")
GRAFICAS_DIR = os.path.join(STATIC_DIR, "graficas")

# Muestra las rutas generadas para verificar que están correctas
print("Base Directory:", BASE_DIR)
print("Ruta de PDFs:", PDF_DIR)
print("Ruta de Gráficas:", GRAFICAS_DIR)

# Asegura que los directorios existan en la ubicación correcta
os.makedirs(PDF_DIR, exist_ok=True)
os.makedirs(GRAFICAS_DIR, exist_ok=True)

def verificar_existencia_archivos(rutas):
#Verifica que los archivos existen, lanzando excepción si falta alguno.
    """Args:
        rutas (list): Lista de rutas de archivos a verificar.
    Raises:
        FileNotFoundError: Si alguno de los archivos no existe.
    """
    for ruta in rutas:
        if not os.path.exists(ruta):
            raise FileNotFoundError(f"No se encontró {ruta}")

def combinar_pdfs(rutas_entrada, ruta_salida):
#combina los PDFs de rutas_entrada y los guarda en ruta_salida
    """ Args:
        rutas_entrada (list): Lista de rutas de los archivos PDF a combinar.
        ruta_salida (str): Ruta donde se guardará el PDF combinado.
    """
    merger = PdfFileMerger()
    try:
        for ruta in rutas_entrada:
            merger.append(ruta)
        with open(ruta_salida, "wb") as f:
            merger.write(f)
    finally:
        merger.close()

def generar_pdf_combinado():
#Genera un PDF combinado con las gráficas y retorna su ruta.
    """ Retorna: str: Ruta del archivo PDF combinado."""
    rutas_entrada = [
        os.path.join("static", "pdf", "Grafico1.pdf"),
        os.path.join("static", "pdf", "Graficocircular.pdf")
    ]
    ruta_salida = os.path.join("static", "pdf", "Graficas.pdf")
    
    verificar_existencia_archivos(rutas_entrada)
    combinar_pdfs(rutas_entrada, ruta_salida)

    return ruta_salida

def descargar_pdf():
#Envía el PDF combinado al usuario como descarga.
    """Retorna: Archivo PDF a descargar o mensaje de error si falla la generación.
    """
    try:
        ruta_salida = generar_pdf_combinado()
        return send_file(ruta_salida, as_attachment=True, download_name="ResultadosGraficas.pdf", mimetype='application/pdf')
    except Exception as e:
        return f"Error al generar el PDF: {str(e)}", 500  # Manejo básico de errores HTTP
