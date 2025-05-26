from flask import Flask, render_template, request, redirect, url_for
import random # Para la semilla global
import numpy as np # Para la semilla global
from typing import Optional


# --- Semilla Global para Reproducibilidad (Opcional) ---
# Si se establece una semilla aquí, afectará al `detector_principal` instanciado abajo,
# haciendo que las secuencias de detección sean las mismas en cada reinicio del servidor.
# Poner None para comportamiento completamente aleatorio.
GLOBAL_APP_SEED = 12345 # Ejemplo de semilla fija
if GLOBAL_APP_SEED is not None:
    print(f"[Servidor] Aplicando semilla global para random y numpy: {GLOBAL_APP_SEED}")
    random.seed(GLOBAL_APP_SEED)
    np.random.seed(GLOBAL_APP_SEED)

# --- Importaciones de Módulos del Proyecto ---
from modules.detector_alimento import DetectorAlimento
from modules.control_cinta import ControlCinta
from modules.cajon import Cajon

# --- Inicialización de la Aplicación Flask ---
app = Flask(__name__, template_folder='templates', static_folder='static')

# --- Instancias Globales ---
# Detector principal (usará la semilla global si se estableció)
detector_principal = DetectorAlimento() # El __init__ del profesor no toma 'seed'
                                        # Se crea el detector independientemente
# Controlador principal de la cinta
controlador_cinta_principal = ControlCinta(detector_alimentos=detector_principal) # Se inyecta

# Último N configurado por el usuario (para pre-rellenar el formulario)
ultimo_N_configurado_usuario: int = 10

# --- Rutas de la Aplicación Web ---
@app.route('/', methods=['GET'])
def index_page():
    global ultimo_N_configurado_usuario
    cajon_a_mostrar: Optional[Cajon] = controlador_cinta_principal.get_ultimo_cajon_procesado()
    return render_template('index.html',
                         cajon_resultado=cajon_a_mostrar,  # El template accede via propiedades
                         n_actual_form=ultimo_N_configurado_usuario)

@app.route('/iniciar_carga_cajon', methods=['POST'])
def iniciar_carga_cajon_action():
    global ultimo_N_configurado_usuario
    num_alimentos_str: Optional[str] = request.form.get('num_alimentos_objetivo_form')
    n_para_este_cajon: int = ultimo_N_configurado_usuario

    if num_alimentos_str and num_alimentos_str.isdigit():
        try:
            n_form = int(num_alimentos_str)
            if n_form > 0:
                n_para_este_cajon = n_form
                ultimo_N_configurado_usuario = n_form
            else:
                app.logger.warning(f"N no positivo: '{num_alimentos_str}'. Usando N={n_para_este_cajon}.")
        except ValueError:
            app.logger.error(f"Error al convertir N: '{num_alimentos_str}'. Usando N={n_para_este_cajon}.")
    else:
        app.logger.warning(f"N no dígito/no provisto: '{num_alimentos_str}'. Usando N={n_para_este_cajon}.")

    app.logger.info(f"Solicitud de carga para N={n_para_este_cajon}.")
    controlador_cinta_principal.procesar_nuevo_cajon(num_alimentos_objetivo=n_para_este_cajon)
    app.logger.info("Procesamiento finalizado. Redirigiendo.")
    return redirect(url_for('index_page'))

# --- Bloque de Ejecución ---
if __name__ == '__main__':
    # app.logger.setLevel(logging.INFO) # Descomentar para más logs de Flask
    app.run(debug=True, port=5000)