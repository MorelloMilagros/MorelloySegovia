# módulo para organizar funciones o clases utilizadas en nuestro proyecto
# Crear tantos módulos como sea necesario para organizar el código

class MonticuloBinarioMin:
    def __init__(self):
        self.listaMonticulo=[0]
        self.tamanoActual=0
    
    def infiltArriba(self,i):
        while i // 2 > 0:
            if self.listaMonticulo[i] < self.listaMonticulo[i // 2] :
                tmp = self.listaMonticulo[i // 2]
                self.listaMonticulo[i // 2] = self.listaMonticulo[i]
                self.listaMonticulo[i] = tmp
            i = i // 2

    def infiltAbajo(self,i):
        while i*2 <= self.tamanoActual:
            hm = self.hijoMin(i)
            if self.listaMonticulo[i] > self.listaMonticulo[hm]:
                tmp = self.listaMonticulo[i]
                self.listaMonticulo[i] = self.listaMonticulo[hm]
                self.listaMonticulo[hm] = tmp
            i = hm

    def hijoMin(self,i):
        if i * 2 + 1 > self.tamanoActual:
            return i * 2
        else:
            if self.listaMonticulo[i*2] < self.listaMonticulo[i*2+1]:
                return i * 2
            else:
                return i * 2 + 1
    
    def insertar(self,k):
        if k is None:
            raise ValueError("No se puede insertar un None en el monticulo")
        self.listaMonticulo.append(k)
        self.tamanoActual = self.tamanoActual + 1
        self.infiltArriba(self.tamanoActual)

    def eliminarMin(self):
        valorSacado = self.listaMonticulo[1]
        self.listaMonticulo[1] = self.listaMonticulo[self.tamanoActual]
        self.tamanoActual = self.tamanoActual - 1
        self.listaMonticulo.pop()
        self.infiltAbajo(1)
        return valorSacado
    
    # def len(self,lista):
    #     self.tamanoActual=len(lista)

    def mostrar(self):
        return self.listaMonticulo[1:]

class MonticuloBinarioMax:
    def __init__(self):
        self.listaMonticulo=[0]
        self.tamanoActual=0
    
    def infiltArribaMax(self, i):
        while i // 2 > 0:
            if self.listaMonticulo[i] > self.listaMonticulo[i // 2]:  # Comparación invertida para montículo de máximos
                self.listaMonticulo[i], self.listaMonticulo[i // 2] = self.listaMonticulo[i // 2], self.listaMonticulo[i]
            i //= 2  # Ajuste del índice

    def infiltAbajo(self,i):
        while i*2 <= self.tamanoActual:
            hm = self.hijoMax(i)
            if self.listaMonticulo[i] < self.listaMonticulo[hm]:
                tmp = self.listaMonticulo[i]
                self.listaMonticulo[i] = self.listaMonticulo[hm]
                self.listaMonticulo[hm] = tmp
            i = hm

    def hijoMax(self,i):
        if i * 2 + 1 > self.tamanoActual:
            return i * 2
        else:
            if self.listaMonticulo[i*2] > self.listaMonticulo[i*2+1]:
                return i * 2
            else:
                return i * 2 + 1
    
    def insertar(self,k):
        if k is None:
            raise ValueError("No se puede insertar un None en el monticulo")
        self.listaMonticulo.append(k)
        self.tamanoActual = self.tamanoActual + 1
        self.infiltArribaMax(self.tamanoActual)

    def eliminarMax(self):
        valorSacado = self.listaMonticulo[1]
        self.listaMonticulo[1] = self.listaMonticulo[self.tamanoActual]
        self.tamanoActual = self.tamanoActual - 1
        self.listaMonticulo.pop()
        self.infiltAbajo(1)
        return valorSacado
    
    # def len(self,lista):
    #     self.tamanoActual=len(lista)

    def mostrar(self):
        return self.listaMonticulo[1:]


class MedianHeap:
    def __init__(self):
        self.monticulo_max = MonticuloBinarioMax()  # Mitad inferior
        self.monticulo_min = MonticuloBinarioMin()  # Mitad superior
        self.mediana = None

    def insertar(self, valor):
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
        if self.mediana is None:
            raise ValueError("No hay suficientes elementos para calcular la mediana")
        return self.mediana
    
if __name__=="__main__":
    mh = MedianHeap()
    valores_prueba = [5, 7, 1, 6, 3, 8, 9]

    for v in valores_prueba:
        mh.insertar(v)
        print(f"Mediana actual después de insertar {v}: {mh.obtener_mediana()}")
    print("Montículo de máximos:", mh.monticulo_max.mostrar())
    print("Montículo de mínimos:", mh.monticulo_min.mostrar())
