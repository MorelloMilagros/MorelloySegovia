import unittest
import os
import sys
import random
import numpy as np
from unittest.mock import MagicMock

# --- Configuración del PYTHONPATH para Pruebas ---
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from modules.detector_alimento import DetectorAlimento # Código del profesor
from modules.clasificador_alimento import (
    Kiwi, Manzana, Papa, Zanahoria, Cajon, crear_objeto_alimento, ControlCinta
)
from server import app as flask_app_instance

# --- Clases de Pruebas Unitarias ---

class TestDetectorAlimentoProfesor(unittest.TestCase):
    """Pruebas para DetectorAlimento (código del profesor)."""

    def setUp(self):
        # Para pruebas deterministas, sembrar ANTES de instanciar.
        random.seed(42)
        np.random.seed(42) # Aunque el detector original no usa np.random directamente para selección
        self.detector = DetectorAlimento()

    def test_output_estructura(self):
        resultado = self.detector.detectar_alimento()
        self.assertIsInstance(resultado, dict)
        self.assertIn("alimento", resultado)
        self.assertIn("peso", resultado)
        self.assertIsInstance(resultado["alimento"], str)
        self.assertIsInstance(resultado["peso"], float)

    def test_valores_esperados(self):
        # Lista de alimentos esperada del detector del profesor
        alimentos_esperados = ["kiwi", "manzana", "papa", "zanahoria", "undefined"]
        pesos_configurados = self.detector.peso_alimentos

        for _ in range(50): # Probar múltiples detecciones
            resultado = self.detector.detectar_alimento()
            self.assertIn(resultado["alimento"], alimentos_esperados)
            # El peso debe ser uno de los `self.peso_alimentos`
            self.assertTrue(any(np.isclose(resultado["peso"], p_cfg) for p_cfg in pesos_configurados),
                            f"Peso detectado {resultado['peso']} no está en la lista de pesos configurados.")

    def test_reproducibilidad_con_semilla_externa(self):
        random.seed(77)
        np.random.seed(77)
        detector1 = DetectorAlimento()
        secuencia1 = [detector1.detectar_alimento() for _ in range(10)]
        
        random.seed(77) # Re-sembrar con la MISMA semilla
        np.random.seed(77)
        detector2 = DetectorAlimento()
        secuencia2 = [detector2.detectar_alimento() for _ in range(10)]
        
        self.assertEqual(secuencia1, secuencia2, "Secuencias deben ser idénticas si la semilla externa es la misma.")

class TestClasificadorYCajon(unittest.TestCase): # Renombrado para claridad
    """Pruebas para Alimento, subclases, crear_objeto_alimento y Cajon."""
    # (Este bloque de pruebas puede permanecer muy similar al anterior,
    # solo asegurar que se usa "undefined" y "papa" correctamente)

    def test_crear_objeto_alimento_con_datos_detector_profesor(self):
        obj_kiwi = crear_objeto_alimento({"alimento": "kiwi", "peso": 0.12})
        self.assertIsInstance(obj_kiwi, Kiwi)

        obj_papa = crear_objeto_alimento({"alimento": "papa", "peso": 0.25}) # "papa" sin tilde
        self.assertIsInstance(obj_papa, Papa)
        self.assertEqual(obj_papa.nombre, "Papa") # La clase Alimento lo normaliza a "Papa"

        obj_undefined = crear_objeto_alimento({"alimento": "undefined", "peso": 0.1}) # "undefined"
        self.assertIsNone(obj_undefined)

    # ... (resto de pruebas para Alimento, Cajon, etc. como en la versión anterior,
    # asegurando consistencia con "undefined" y "papa")
    def test_creacion_alimentos_y_calculo_aw(self):
        kiwi = Kiwi(0.1)
        self.assertAlmostEqual(kiwi.calcular_aw(), 0.139292, places=5)
        papa_limite = Papa(0.6) 
        self.assertEqual(papa_limite.calcular_aw(), 1.0)
        with self.assertRaisesRegex(ValueError, "debe ser un número positivo"): Kiwi(0)

    def test_cajon_calculo_metricas_y_advertencias(self):
        cajon = Cajon(3)
        k1 = Kiwi(0.1); m1 = Manzana(0.15); p1_grande = Papa(0.6) # Papa dará aw=1.0
        cajon.agregar_alimento(k1); cajon.agregar_alimento(m1); cajon.agregar_alimento(p1_grande)
        cajon.calcular_metricas()
        self.assertTrue("¡ADVERTENCIA!" in cajon.advertencia)
        self.assertTrue("AW Promedio Papa (1.000) > 0.90" in cajon.advertencia)
        self.assertTrue("AW Promedio Verdura (1.000) > 0.90" in cajon.advertencia)


class TestControlCintaConDetectorProfesor(unittest.TestCase):
    """Pruebas para ControlCinta usando el DetectorAlimento del profesor."""

    def setUp(self):
        # Sembrar antes de cada prueba para ControlCinta para que el detector sea predecible
        random.seed(101)
        np.random.seed(101)
        self.detector_para_control = DetectorAlimento() # Usa el detector del profesor
        self.control_cinta = ControlCinta(detector_alimentos=self.detector_para_control)

    def test_procesar_llena_cajon_con_N_validos(self):
        N_objetivo = 3
        # Con seed 101, la secuencia del detector del profesor es:
        # 1. {'alimento': 'papa', 'peso': 0.49} -> Papa
        # 2. {'alimento': 'kiwi', 'peso': 0.16} -> Kiwi
        # 3. {'alimento': 'undefined', 'peso': 0.33} -> descarta
        # 4. {'alimento': 'undefined', 'peso': 0.27} -> descarta
        # 5. {'alimento': 'zanahoria', 'peso': 0.33} -> Zanahoria (tercer válido)
        cajon = self.control_cinta.procesar_nuevo_cajon(N_objetivo)
        self.assertEqual(cajon.get_num_alimentos(), N_objetivo, 
                         f"Esperaba {N_objetivo} válidos, obtuvo {cajon.get_num_alimentos()}")
        nombres_en_cajon = [al.nombre for al in cajon.alimentos_en_cajon]
        self.assertIn("Papa", nombres_en_cajon)
        self.assertIn("Kiwi", nombres_en_cajon)
        self.assertIn("Zanahoria", nombres_en_cajon)

    # ... (otras pruebas para ControlCinta como `test_get_ultimo_cajon_procesado`
    # y `test_procesar_cajon_con_N_invalido_usa_default` pueden permanecer similares)
    def test_get_ultimo_cajon_actualiza_estado(self):
        self.assertIsNone(self.control_cinta.get_ultimo_cajon_procesado())
        cajon1 = self.control_cinta.procesar_nuevo_cajon(1)
        self.assertIs(self.control_cinta.get_ultimo_cajon_procesado(), cajon1)


class TestFlaskRutasConDetectorProfesor(unittest.TestCase):
    """Pruebas de integración para las rutas Flask."""

    @classmethod
    def setUpClass(cls):
        flask_app_instance.config['TESTING'] = True
        flask_app_instance.config['WTF_CSRF_ENABLED'] = False
        # La semilla global en server.py (si se establece) controlará el detector_principal.
        # Si server.py tiene GLOBAL_APP_SEED = 12345, las pruebas de ruta serán deterministas.

    def setUp(self):
        self.client = flask_app_instance.test_client()
        # Reiniciar el estado del controlador para cada prueba de ruta
        from server import controlador_cinta_principal, detector_principal
        # El detector_principal ya está instanciado y afectado (o no) por la semilla en server.py
        controlador_cinta_principal.__init__(detector_alimentos=detector_principal)
        # Reiniciar el N global de server.py si es necesario
        # (Esto se hace para aislar las pruebas de efectos secundarios del N)
        # from server import ultimo_N_configurado_usuario
        # Acceder a globales de otro módulo para modificar es delicado, pero para tests a veces se hace.
        # Si 'server' es el nombre del archivo, se puede importar y modificar.
        import server
        server.ultimo_N_configurado_usuario = 10


    def test_ruta_index_carga_inicial(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Control Cinta Transportadora", response.data)
        self.assertIn(b"A\xc3\xban no se ha procesado ning\xc3\xban caj\xc3\xb3n", response.data) # "Aún no se ha procesado ningún cajón"

    def test_ruta_iniciar_carga_funciona_y_muestra_resultados(self):
        N_prueba = 2
        # Con GLOBAL_APP_SEED = 12345 en server.py, el detector_principal dará:
        # 1. {'alimento': 'papa', 'peso': 0.22} -> Papa
        # 2. {'alimento': 'kiwi', 'peso': 0.16} -> Kiwi
        # ... (y así sucesivamente)
        response_post = self.client.post('/iniciar_carga_cajon',
                                         data={'num_alimentos_objetivo_form': str(N_prueba)})
        self.assertEqual(response_post.status_code, 302) # Redirección

        response_get = self.client.get(response_post.location)
        self.assertEqual(response_get.status_code, 200)
        self.assertIn(b"Resultados del \xc3\x9altimo Caj\xc3\xb3n Procesado", response_get.data)
        self.assertIn(f"Capacidad M\xc3\xa1xima (N configurado):</strong> {N_prueba}".encode('utf-8'), response_get.data)
        # Verificar que al menos un alimento específico se muestre (depende de la semilla)
        self.assertIn(b"Papa:", response_get.data) # Si la semilla 12345 produce una papa primero
        self.assertIn(b"Kiwi:", response_get.data) # Y luego un kiwi

# --- Ejecución de Pruebas ---
if __name__ == '__main__':
    unittest.main(verbosity=2)