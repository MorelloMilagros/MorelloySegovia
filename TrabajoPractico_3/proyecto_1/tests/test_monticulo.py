# tests/test_monticulo.py

# 1. Importamos la clase que queremos probar desde tu módulo
from modules.monticulo_binario import MedianHeap

def test_mediana_con_numeros_impares():
    """
    Verifica que tu clase MedianHeap calcule la mediana correcta
    cuando se inserta una cantidad impar de elementos.
    """
    # ARRANGE (Preparar): Creamos una instancia de tu clase
    # y la lista de números a probar.
    median_heap = MedianHeap()
    numeros = [10, 4, 15, 2, 8]  # La mediana de [2, 4, 8, 10, 15] es 8

    # ACT (Actuar): Insertamos todos los números
    for n in numeros:
        median_heap.insertar(n)

    # ASSERT (Afirmar): Comprobamos que el resultado es el esperado
    mediana_calculada = median_heap.obtener_mediana()
    assert mediana_calculada == 8
def test_mediana_con_numeros_pares():
    """
    Verifica que tu clase MedianHeap calcule la mediana correcta
    cuando se inserta una cantidad par de elementos.
    """
    # ARRANGE (Preparar)
    median_heap = MedianHeap()
    numeros = [10, 4, 15, 2, 8, 20] # Ordenados: [2, 4, 8, 10, 15, 20]. Mediana: (8+10)/2 = 9

    # ACT (Actuar)
    for n in numeros:
        median_heap.insertar(n)

    # ASSERT (Afirmar)
    mediana_calculada = median_heap.obtener_mediana()
    assert mediana_calculada == 9.0