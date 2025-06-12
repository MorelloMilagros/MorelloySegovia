# tests/test_algoritmos.py
import pytest
from modules.monticulo_binario import MedianHeap

def test_mediana_con_numeros_impares():
    """Verifica que MedianHeap calcule la mediana correcta con una cantidad impar de elementos."""
    median_heap = MedianHeap()
    numeros = [10, 4, 15, 2, 8]  # La mediana de [2, 4, 8, 10, 15] es 8
    for n in numeros:
        median_heap.insertar(n)
    assert median_heap.obtener_mediana() == 8

def test_mediana_con_numeros_pares():
    """Verifica que MedianHeap calcule la mediana correcta con una cantidad par de elementos."""
    median_heap = MedianHeap()
    numeros = [10, 4, 15, 2, 8, 20] # Ordenados: [2, 4, 8, 10, 15, 20]. Mediana: (8+10)/2 = 9
    for n in numeros:
        median_heap.insertar(n)
    assert median_heap.obtener_mediana() == 9.0

def test_mediana_con_numeros_ordenados():
    """Verifica que el cálculo sea correcto con números ya ordenados."""
    median_heap = MedianHeap()
    numeros = [1, 2, 3, 4, 5, 6] # Mediana (3+4)/2 = 3.5
    for n in numeros:
        median_heap.insertar(n)
    assert median_heap.obtener_mediana() == 3.5
    
def test_mediana_vacia_falla():
    """Verifica que obtener la mediana de un montículo vacío lance un error."""
    median_heap = MedianHeap()
    with pytest.raises(ValueError, match="No hay suficientes elementos para calcular la mediana"):
        median_heap.obtener_mediana()