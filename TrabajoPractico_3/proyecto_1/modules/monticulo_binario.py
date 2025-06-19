# módulo para organizar funciones o clases utilizadas en nuestro proyecto
# Crear tantos módulos como sea necesario para organizar el código
"""
Este módulo implementa estructuras de datos de montículos binarios (Min-Heap y Max-Heap)
y una estructura combinada (MedianHeap) para calcular eficientemente la mediana
de un flujo de números.

Contiene las siguientes clases:
- `MonticuloBinarioMin`: Implementa un min-heap.
- `MonticuloBinarioMax`: Implementa un max-heap.
- `MedianHeap`: Utiliza ambos montículos para mantener y calcular la mediana.
"""
class MonticuloBinarioMin:
    """
    Implementación de un montículo binario de mínimos (Min-Heap).

    Un Min-Heap es una estructura de datos de árbol binario que satisface
    la propiedad de heap-mínimo: el valor de cada nodo es menor o igual
    que el valor de sus hijos. El elemento más pequeño está siempre en la raíz.

    Atributos:
        listaMonticulo (list): Lista que representa el montículo, donde el índice 0 se ignora.
                               El elemento en el índice 1 es la raíz.
        tamanoActual (int): El número actual de elementos en el montículo.
    """
    def __init__(self):
        """Inicializa un montículo binario de mínimos vacío."""
        self.listaMonticulo=[0]
        self.tamanoActual=0
    
    def infiltArriba(self,i):
        """
        Mueve un elemento hacia arriba en el montículo para mantener la propiedad de Min-Heap.

        Se usa después de insertar un nuevo elemento para reajustar su posición.
        Compara el elemento en el índice `i` con su padre y los intercambia si es necesario.

        Args:
            i (int): El índice del elemento a "infiltrar" hacia arriba.
        """
        while i // 2 > 0:
            if self.listaMonticulo[i] < self.listaMonticulo[i // 2] :
                tmp = self.listaMonticulo[i // 2]
                self.listaMonticulo[i // 2] = self.listaMonticulo[i]
                self.listaMonticulo[i] = tmp
            i = i // 2

    def infiltAbajo(self,i):
        """
        Mueve un elemento hacia abajo en el montículo para mantener la propiedad de Min-Heap.

        Se usa después de eliminar la raíz (el mínimo) para reajustar el montículo.
        Compara el elemento en el índice `i` con sus hijos y lo intercambia con el menor.

        Args:
            i (int): El índice del elemento a "infiltrar" hacia abajo.
        """
        while i*2 <= self.tamanoActual:
            hm = self.hijoMin(i)
            if self.listaMonticulo[i] > self.listaMonticulo[hm]:
                tmp = self.listaMonticulo[i]
                self.listaMonticulo[i] = self.listaMonticulo[hm]
                self.listaMonticulo[hm] = tmp
            i = hm

    def hijoMin(self,i):
        """
        Devuelve el índice del hijo con el valor mínimo del nodo en el índice `i`.

        Args:
            i (int): El índice del nodo padre.

        Returns:
            int: El índice del hijo con el valor más pequeño.
        """
        if i * 2 + 1 > self.tamanoActual:
            return i * 2
        else:
            if self.listaMonticulo[i*2] < self.listaMonticulo[i*2+1]:
                return i * 2
            else:
                return i * 2 + 1
    
    def insertar(self,k):
        """
        Inserta un nuevo elemento en el montículo de mínimos.

        El elemento se añade al final y luego se "infiltra" hacia arriba
        para mantener la propiedad del montículo.

        Args:
            k (numeric): El valor numérico a insertar.

        Raises:
            ValueError: Si se intenta insertar un valor None.
        """
        if k is None:
            raise ValueError("No se puede insertar un None en el monticulo")
        self.listaMonticulo.append(k)
        self.tamanoActual = self.tamanoActual + 1
        self.infiltArriba(self.tamanoActual)

    def eliminarMin(self):
        """
        Elimina y retorna el elemento mínimo (la raíz) del montículo.

        El último elemento se mueve a la raíz y luego se "infiltra" hacia abajo
        para reajustar el montículo.

        Returns:
            numeric: El valor mínimo que fue eliminado.
        """
        valorSacado = self.listaMonticulo[1]
        self.listaMonticulo[1] = self.listaMonticulo[self.tamanoActual]
        self.tamanoActual = self.tamanoActual - 1
        self.listaMonticulo.pop()
        self.infiltAbajo(1)
        return valorSacado
    
    # def len(self,lista):
    #     self.tamanoActual=len(lista)

    def mostrar(self):
        """
        Retorna una lista con los elementos del montículo (excluyendo el marcador inicial).

        Returns:
            list: Lista de los elementos en el montículo.
        """
        return self.listaMonticulo[1:]

class MonticuloBinarioMax:
    """
    Implementación de un montículo binario de máximos (Max-Heap).

    Un Max-Heap es una estructura de datos de árbol binario que satisface
    la propiedad de heap-máximo: el valor de cada nodo es mayor o igual
    que el valor de sus hijos. El elemento más grande está siempre en la raíz.

    Atributos:
        listaMonticulo (list): Lista que representa el montículo, donde el índice 0 se ignora.
                               El elemento en el índice 1 es la raíz.
        tamanoActual (int): El número actual de elementos en el montículo.
    """
    def __init__(self):
        """Inicializa un montículo binario de máximos vacío."""
        self.listaMonticulo=[0]
        self.tamanoActual=0
    
    def infiltArribaMax(self, i):
        """
        Mueve un elemento hacia arriba en el montículo para mantener la propiedad de Max-Heap.

        Similar a `infiltArriba` de Min-Heap, pero compara para el máximo.

        Args:
            i (int): El índice del elemento a "infiltrar" hacia arriba.
        """
        while i // 2 > 0:
            if self.listaMonticulo[i] > self.listaMonticulo[i // 2]:  # Comparación invertida para montículo de máximos
                self.listaMonticulo[i], self.listaMonticulo[i // 2] = self.listaMonticulo[i // 2], self.listaMonticulo[i]
            i //= 2  # Ajuste del índice

    def infiltAbajo(self,i):
        """
        Mueve un elemento hacia abajo en el montículo para mantener la propiedad de Max-Heap.

        Similar a `infiltAbajo` de Min-Heap, pero compara para el máximo.

        Args:
            i (int): El índice del elemento a "infiltrar" hacia abajo.
        """
        while i*2 <= self.tamanoActual:
            hm = self.hijoMax(i)
            if self.listaMonticulo[i] < self.listaMonticulo[hm]:
                tmp = self.listaMonticulo[i]
                self.listaMonticulo[i] = self.listaMonticulo[hm]
                self.listaMonticulo[hm] = tmp
            i = hm

    def hijoMax(self,i):
        """
        Devuelve el índice del hijo con el valor máximo del nodo en el índice `i`.

        Args:
            i (int): El índice del nodo padre.

        Returns:
            int: El índice del hijo con el valor más grande.
        """
        if i * 2 + 1 > self.tamanoActual:
            return i * 2
        else:
            if self.listaMonticulo[i*2] > self.listaMonticulo[i*2+1]:
                return i * 2
            else:
                return i * 2 + 1
    
    def insertar(self,k):
        """
        Inserta un nuevo elemento en el montículo de máximos.

        El elemento se añade al final y luego se "infiltra" hacia arriba.

        Args:
            k (numeric): El valor numérico a insertar.

        Raises:
            ValueError: Si se intenta insertar un valor None.
        """
        if k is None:
            raise ValueError("No se puede insertar un None en el monticulo")
        self.listaMonticulo.append(k)
        self.tamanoActual = self.tamanoActual + 1
        self.infiltArribaMax(self.tamanoActual)

    def eliminarMax(self):
        """
        Elimina y retorna el elemento máximo (la raíz) del montículo.

        El último elemento se mueve a la raíz y luego se "infiltra" hacia abajo.

        Returns:
            numeric: El valor máximo que fue eliminado.
        """
        valorSacado = self.listaMonticulo[1]
        self.listaMonticulo[1] = self.listaMonticulo[self.tamanoActual]
        self.tamanoActual = self.tamanoActual - 1
        self.listaMonticulo.pop()
        self.infiltAbajo(1)
        return valorSacado
    
    # def len(self,lista):
    #     self.tamanoActual=len(lista)

    def mostrar(self):
        """
        Retorna una lista con los elementos del montículo (excluyendo el marcador inicial).

        Returns:
            list: Lista de los elementos en el montículo.
        """
        return self.listaMonticulo[1:]


class MedianHeap:
    """
    Estructura de datos para calcular la mediana de un flujo de números de forma eficiente.

    Utiliza dos montículos binarios:
    - `monticulo_max` (Max-Heap): Almacena la mitad inferior de los números. La raíz es el elemento más grande de la mitad inferior.
    - `monticulo_min` (Min-Heap): Almacena la mitad superior de los números. La raíz es el elemento más pequeño de la mitad superior.

    Al mantener los tamaños de ambos montículos equilibrados (o con una diferencia máxima de 1),
    la mediana siempre será la raíz del montículo más grande o el promedio de las dos raíces
    si ambos montículos tienen el mismo tamaño.

    Atributos:
        monticulo_max (MonticuloBinarioMax): Montículo para los números menores o iguales a la mediana.
        monticulo_min (MonticuloBinarioMin): Montículo para los números mayores o iguales a la mediana.
        mediana (numeric or None): El valor de la mediana calculada, o None si no hay suficientes elementos.
    """
    def __init__(self):
        """Inicializa una instancia de MedianHeap."""
        self.monticulo_max = MonticuloBinarioMax()  # Mitad inferior
        self.monticulo_min = MonticuloBinarioMin()  # Mitad superior
        self.mediana = None

    def insertar(self, valor):
        """
        Inserta un nuevo valor en el MedianHeap y actualiza la mediana.

        La inserción se realiza de manera que los montículos se mantengan
        equilibrados para calcular la mediana en O(log n) tiempo.

        Args:
            valor (numeric): El número a insertar.

        Raises:
            ValueError: Si se intenta insertar un valor None.
        """
        if self.mediana is None:  # Primer elemento
            self.mediana = valor
            self.monticulo_max.insertar(valor)
            return
        
        if valor <= self.mediana:
            self.monticulo_max.insertar(valor)
        else:
            self.monticulo_min.insertar(valor)

        # Rebalanceo si la diferencia de tamaño es mayor a 1
        if self.monticulo_max.tamanoActual > self.monticulo_min.tamanoActual + 1:
            self.monticulo_min.insertar(self.monticulo_max.eliminarMax())
        elif self.monticulo_min.tamanoActual > self.monticulo_max.tamanoActual + 1:
            self.monticulo_max.insertar(self.monticulo_min.eliminarMin())

        print("Montículo de máximos completo:", self.monticulo_max.listaMonticulo)
        print("Montículo de mínimos completo:", self.monticulo_min.listaMonticulo)

        print(f"Tamaño montículo_max: {self.monticulo_max.tamanoActual}")
        print(f"Tamaño montículo_min: {self.monticulo_min.tamanoActual}")

        # Actualizar la mediana
        if self.monticulo_max.tamanoActual == self.monticulo_min.tamanoActual:
            self.mediana = (self.monticulo_max.listaMonticulo[1] + self.monticulo_min.listaMonticulo[1]) / 2
        elif self.monticulo_max.tamanoActual > self.monticulo_min.tamanoActual:
            self.mediana = self.monticulo_max.listaMonticulo[1]  # La raíz siempre debe ser el mayor de los menores
        else:
            self.mediana = self.monticulo_min.listaMonticulo[1]  # La raíz siempre debe ser el menor de los mayores


    def obtener_mediana(self):
        """
        Retorna la mediana actual de los números insertados en el heap.

        Returns:
            numeric: El valor de la mediana.

        Raises:
            ValueError: Si no hay suficientes elementos para calcular la mediana (es decir, el heap está vacío).
        """
        if self.mediana is None:
            raise ValueError("No hay suficientes elementos para calcular la mediana")
        return self.mediana
    
if __name__=="__main__":
    """
    Bloque de prueba para la clase MedianHeap.

    Este código se ejecuta solo cuando 'monticulo_binario.py' es ejecutado directamente.
    Inserta una serie de valores y muestra la mediana después de cada inserción,
    demostrando el funcionamiento de la estructura.
    """
    mh = MedianHeap()
    valores_prueba = [5, 7, 1, 6, 3, 8, 9]

    for v in valores_prueba:
        mh.insertar(v)
        print(f"Mediana actual después de insertar {v}: {mh.obtener_mediana()}")
    print("Montículo de máximos:", mh.monticulo_max.mostrar())
    print("Montículo de mínimos:", mh.monticulo_min.mostrar())
