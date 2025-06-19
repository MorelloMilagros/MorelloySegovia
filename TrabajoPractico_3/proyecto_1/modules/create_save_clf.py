from modules.classifier import ClaimsClassifier
from modules.create_csv import crear_csv
import pickle

datos = crear_csv("./data/frases.json")
X = datos['reclamo']
y = datos['etiqueta']

clf = ClaimsClassifier()
clf.fit(X, y)

with open('./data/claims_clf.pkl', 'wb') as archivo:
    pickle.dump(clf, archivo)
"""
Script para entrenar y guardar el clasificador de reclamos.

Este script realiza los siguientes pasos:
1. Carga los datos de entrenamiento de reclamos desde './data/frases.json'
   utilizando la función `crear_csv`.
2. Inicializa una instancia de `ClaimsClassifier`.
3. Entrena el clasificador con los reclamos y sus etiquetas.
4. Serializa (guarda) el clasificador entrenado en un archivo binario
   './data/claims_clf.pkl' utilizando `pickle`, para que pueda ser
   cargado y utilizado por la aplicación principal sin necesidad de
   volver a entrenarlo cada vez.
"""