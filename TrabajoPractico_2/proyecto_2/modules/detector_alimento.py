import numpy as np
import random
import matplotlib.pyplot as plt
from abc import ABC, abstractmethod


class DetectorAlimento:
    """clase que representa un conjunto de sensores de la cinta transportadora
    para detectar el tipo de alimento y su peso.
    """
    def __init__(self):
        self.alimentos = ["kiwi", "manzana", "papa", "zanahoria", "undefined"] # papa sin tilde, undefined
        self.peso_alimentos = np.round(np.linspace(0.05, 0.6, 12),2)
        # Es importante notar que después de round(), la suma de prob_pesos puede no ser exactamente 1.
        # random.choices normaliza internamente los pesos si son positivos.
        self.prob_pesos = np.round(self.__softmax(self.peso_alimentos)[::-1], 2)

    def __softmax(self, x):
        """función softmax para crear vector de probabilidades 
        que sumen 1 en total
        """
        # Estabilidad numérica: restar max(x) antes de exp()
        exp_x = np.exp(x - np.max(x))
        return exp_x / exp_x.sum()

    def detectar_alimento(self):
        """método que simula la detección del alimento y devuelve un diccionario
        con la información del tipo y el peso del alimento.
        """
        n_alimentos = len(self.alimentos)
        # Selección uniforme del tipo de alimento
        alimento_detectado = self.alimentos[random.randint(0, n_alimentos-1)]
        # Selección de peso según self.prob_pesos
        # random.choices espera una secuencia de pesos (weights), no necesariamente normalizada a 1
        # si todos los pesos son positivos, los normaliza internamente.
        # Si prob_pesos contiene valores negativos o todos son cero, puede dar error.
        # Asumimos que self.prob_pesos serán positivos después del softmax y redondeo.
        try:
            peso_detectado = random.choices(self.peso_alimentos, weights=self.prob_pesos, k=1)[0]
        except ValueError as e:
            # Esto podría ocurrir si todos los prob_pesos son cero después del redondeo,
            # o si hay algún negativo (improbable con softmax).
            # Fallback a una selección uniforme de peso si random.choices falla.
            print(f"ADVERTENCIA: random.choices falló con prob_pesos ({e}). Usando selección uniforme de peso.")
            peso_detectado = random.choice(self.peso_alimentos)

        return {"alimento": alimento_detectado, "peso": float(peso_detectado)} # Asegurar que el peso es float

if __name__ == "__main__":
    random.seed(1) # Semilla para la ejecución de este script de prueba
    # numpy también tiene su propio generador, si se usara np.random directamente.
    # np.random.seed(1) 
    
    sensor = DetectorAlimento()
    print(f"Probabilidades de pesos (pueden no sumar 1 exacto por redondeo): {sensor.prob_pesos}")
    print(f"Suma de probabilidades de pesos: {np.sum(sensor.prob_pesos)}")
    
    lista_pesos_detectados = []
    alimentos_contados = {nombre: 0 for nombre in sensor.alimentos}
    
    for i in range(200):
        detectado = sensor.detectar_alimento()
        #Solo agregar pesos de alimentos definidos para el histograma, aunque el detector original no lo hacía.
        #Para replicar el original, se deberían agregar todos.
        #if detectado["alimento"] != "undefined":
        lista_pesos_detectados.append(detectado["peso"])
        alimentos_contados[detectado["alimento"]] += 1
        if i < 5: # Mostrar algunas detecciones
            print(detectado)

    print("\nConteo de alimentos detectados:")
    for alimento, conteo in alimentos_contados.items():
        print(f"  {alimento}: {conteo}")

    if lista_pesos_detectados:
        plt.hist(lista_pesos_detectados, bins=len(sensor.peso_alimentos), edgecolor='black')
        plt.title("Distribución de Pesos Detectados (Todos los alimentos)")
        plt.xlabel("Peso (kg)")
        plt.ylabel("Frecuencia")
        plt.grid(axis='y', alpha=0.75)
        plt.show()
    else:
        print("No se detectaron pesos.")