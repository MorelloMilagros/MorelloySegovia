import unittest
import os
import sys
import random
import numpy as np
from unittest.mock import MagicMock, patch
from io import StringIO
from modules.detector_alimento import DetectorAlimento
from modules.alimento import (Alimento, Fruta, Verdura,
                            Kiwi, Manzana, Papa, Zanahoria)
from modules.cajon import Cajon
from modules.control_cinta import ControlCinta
from server import app as flask_app

class TestAlimentoBase(unittest.TestCase):
    def test_alimento_abstract(self):
        with self.assertRaises(TypeError):
            Alimento("abstract", 0.1)
            
    def test_str_alimento(self):
        kiwi = Kiwi(0.1)
        self.assertIn("Kiwi", str(kiwi))
        self.assertIn("Fruta", str(kiwi))
        self.assertIn("0.100", str(kiwi))

class TestFrutas(unittest.TestCase):
    def test_kiwi(self):
        kiwi = Kiwi(0.1)
        self.assertEqual(kiwi.nombre, "Kiwi")
        self.assertEqual(kiwi.tipo_alimento, "Fruta")
        self.assertAlmostEqual(kiwi.calcular_aw(), 0.688, places=3)
        
        kiwi_grande = Kiwi(0.6)
        self.assertEqual(kiwi_grande.calcular_aw(), 1.0)

    def test_manzana(self):
        manzana = Manzana(0.2)
        self.assertEqual(manzana.nombre, "Manzana")
        self.assertAlmostEqual(manzana.calcular_aw(), 0.873, places=3)

class TestVerduras(unittest.TestCase):
    def test_papa(self):
        papa = Papa(0.3)
        self.assertEqual(papa.nombre, "Papa")
        self.assertEqual(papa.tipo_alimento, "Verdura")
        self.assertAlmostEqual(papa.calcular_aw(), 0.916, places=3)

    def test_zanahoria(self):
        zanahoria = Zanahoria(0.15)
        self.assertAlmostEqual(zanahoria.calcular_aw(), 0.746, places=3)

class TestCajon(unittest.TestCase):
    def setUp(self):
        self.cajon = Cajon(5)
        self.kiwi = Kiwi(0.1)
        self.manzana = Manzana(0.2)
        self.papa = Papa(0.3)

    def test_agregar_alimento(self):
        self.assertTrue(self.cajon.agregar_alimento(self.kiwi))
        self.assertEqual(self.cajon.get_num_alimentos(), 1)
        
    def test_cajon_lleno(self):
        for _ in range(5):
            self.cajon.agregar_alimento(self.kiwi)
        self.assertTrue(self.cajon.esta_lleno())
        self.assertFalse(self.cajon.agregar_alimento(self.kiwi))

    def test_calcular_metricas(self):
        self.cajon.agregar_alimento(self.kiwi)
        self.cajon.agregar_alimento(self.manzana)
        self.cajon.agregar_alimento(self.papa)
        
        self.cajon.calcular_metricas()
        
        self.assertAlmostEqual(self.cajon.peso_total_kg, 0.6, places=2)
        self.assertIn("Fruta", self.cajon.aw_prom_por_tipo)
        self.assertIn("Kiwi", self.cajon.aw_prom_por_alimento)

    def test_iteracion(self):
        self.cajon.agregar_alimento(self.kiwi)
        self.cajon.agregar_alimento(self.manzana)
        alimentos = list(self.cajon)
        self.assertEqual(len(alimentos), 2)
        
    def test_str_cajon(self):
        self.cajon.agregar_alimento(self.kiwi)
        cajon_str = str(self.cajon)
        self.assertIn("ESTADO DEL CAJÓN", cajon_str)
        self.assertIn("Kiwi", cajon_str)

class TestControlCinta(unittest.TestCase):
    def setUp(self):
        # Crear el mock del detector
        self.detector_mock = MagicMock(spec=DetectorAlimento)
        # Inicializar el control con el mock
        self.control = ControlCinta(self.detector_mock)  # Usar self.detector_mock

    def test_procesar_cajon(self):
    # Configurar el mock para devolver una secuencia que incluya todos los alimentos
        self.detector_mock.detectar_alimento.side_effect = [
            {"alimento": "kiwi", "peso": 0.1},
            {"alimento": "undefined", "peso": 0.2},
            {"alimento": "manzana", "peso": 0.2},
            {"alimento": "undefined", "peso": 0.3},
            {"alimento": "papa", "peso": 0.3},
            {"alimento": "zanahoria", "peso": 0.15}  # Nuevo: agregamos zanahoria
        ]
    
    # Mockear el método interno de creación de alimentos
        with patch.object(ControlCinta, '_crear_objeto_alimento') as mock_crear:
            mock_crear.side_effect = [
                Kiwi(0.1),      # kiwi
                None,           # undefined
                Manzana(0.2),   # manzana
                None,           # undefined
                Papa(0.3),      # papa
                Zanahoria(0.15) # zanahoria (nuevo)
            ]
        
            # Procesamos un cajón con capacidad para 4 alimentos (ahora incluimos zanahoria)
            cajon = self.control.procesar_nuevo_cajon(4)
            
            # Verificaciones
            self.assertEqual(cajon.get_num_alimentos(), 4)
            
            # Verificar que todos los tipos de alimentos están presentes
            alimentos_en_cajon = list(cajon)
            tipos_presentes = {a.tipo_alimento for a in alimentos_en_cajon}
            self.assertIn("Fruta", tipos_presentes)
            self.assertIn("Verdura", tipos_presentes)
            
            # Verificar nombres específicos
            nombres_presentes = {a.nombre for a in alimentos_en_cajon}
            self.assertIn("Kiwi", nombres_presentes)
            self.assertIn("Manzana", nombres_presentes)
            self.assertIn("Papa", nombres_presentes)
            self.assertIn("Zanahoria", nombres_presentes)

    def test_ultimo_cajon(self):
        self.assertIsNone(self.control.get_ultimo_cajon_procesado())
        
        # Configurar el mock
        self.detector_mock.detectar_alimento.return_value = {"alimento": "kiwi", "peso": 0.1}
        
        # Mockear el método interno
        with patch.object(ControlCinta, '_crear_objeto_alimento', return_value=Kiwi(0.1)):
            cajon = self.control.procesar_nuevo_cajon(1)
            self.assertEqual(self.control.get_ultimo_cajon_procesado(), cajon)

class TestFlaskApp(unittest.TestCase):
    def setUp(self):
        self.app = flask_app.test_client()
        self.app.testing = True

    def test_index(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Cinta Transportadora", response.data)

    def test_iniciar_carga(self):
        with patch('server.controlador_cinta_principal') as mock_control:
            mock_cajon = MagicMock()
            mock_cajon.get_num_alimentos.return_value = 2
            mock_control.procesar_nuevo_cajon.return_value = mock_cajon
        
            response = self.app.post('/iniciar_carga_cajon', data={
                'num_alimentos_objetivo_form': '3'
            })
        
            self.assertEqual(response.status_code, 302)        
            mock_control.procesar_nuevo_cajon.assert_called_once()
            args, kwargs = mock_control.procesar_nuevo_cajon.call_args
            self.assertEqual(kwargs.get('num_alimentos_objetivo'), 3)

class TestFactory(unittest.TestCase):
    def setUp(self):
        self.control = ControlCinta(MagicMock(spec=DetectorAlimento))

    def test_crear_objeto_valido(self):
        alimento = self.control._crear_objeto_alimento({"alimento": "kiwi", "peso": 0.1})
        self.assertIsInstance(alimento, Kiwi)

    def test_crear_undefined(self):
        alimento = self.control._crear_objeto_alimento({"alimento": "undefined", "peso": 0.1})
        self.assertIsNone(alimento)

    def test_crear_invalido(self):
        alimento = self.control._crear_objeto_alimento({"alimento": "desconocido", "peso": 0.1})
        self.assertIsNone(alimento)

class TestDetectorAlimento(unittest.TestCase):
    def setUp(self):
        random.seed(42)  # Para pruebas deterministas
        self.detector = DetectorAlimento()

    def test_detector_estructura(self):
        resultado = self.detector.detectar_alimento()
        self.assertIsInstance(resultado, dict)
        self.assertIn("alimento", resultado)
        self.assertIn("peso", resultado)
        
    def test_detector_valores_validos(self):
        for _ in range(10):  # Probamos múltiples veces
            resultado = self.detector.detectar_alimento()
            self.assertIn(resultado["alimento"], ["kiwi", "manzana", "papa", "zanahoria", "undefined"])
            self.assertTrue(0.05 <= resultado["peso"] <= 0.6)

if __name__ == '__main__':
    unittest.main(verbosity=2)