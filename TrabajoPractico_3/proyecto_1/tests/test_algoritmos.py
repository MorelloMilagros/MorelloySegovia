# tests/test_algoritmos.py
import unittest
from modules.monticulo_binario import MedianHeap

class TestAlgoritmos(unittest.TestCase):

    def test_mediana_vacia_falla(self):
        """Prueba que obtener la mediana de un montículo vacío lance un error."""
        mh = MedianHeap()
        with self.assertRaisesRegex(ValueError, "No hay suficientes elementos para calcular la mediana"):
            mh.obtener_mediana()

    def test_mediana_un_elemento(self):
        mh = MedianHeap()
        mh.insertar(10)
        self.assertEqual(mh.obtener_mediana(), 10)

    def test_mediana_dos_elementos(self):
        mh = MedianHeap()
        mh.insertar(10)
        mh.insertar(20)
        self.assertEqual(mh.obtener_mediana(), 15.0)

    def test_mediana_impar(self):
        mh = MedianHeap()
        numeros = [5, 1, 10, 2, 7] # Ordenado: [1, 2, 5, 7, 10] -> Mediana: 5
        for n in numeros:
            mh.insertar(n)
        self.assertEqual(mh.obtener_mediana(), 5)

    def test_mediana_par(self):
        mh = MedianHeap()
        numeros = [5, 1, 10, 2, 7, 12] # Ordenado: [1, 2, 5, 7, 10, 12] -> Mediana: (5+7)/2 = 6
        for n in numeros:
            mh.insertar(n)
        self.assertEqual(mh.obtener_mediana(), 6.0)

    def test_mediana_flujo_continuo(self):
        mh = MedianHeap()
        mh.insertar(5)
        self.assertEqual(mh.obtener_mediana(), 5)
        mh.insertar(1)
        self.assertEqual(mh.obtener_mediana(), 3.0)
        mh.insertar(10)
        self.assertEqual(mh.obtener_mediana(), 5)
        mh.insertar(2)
        self.assertEqual(mh.obtener_mediana(), 3.5)
        mh.insertar(7)
        self.assertEqual(mh.obtener_mediana(), 5)
        
if __name__ == '__main__':
    unittest.main()