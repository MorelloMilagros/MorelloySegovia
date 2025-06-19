import json
import pandas as pd

def crear_csv(direccion):
  with open(direccion,'r', encoding='utf-8') as f:
    datos_entrenamiento = json.load(f)

  reclamos = [i['reclamo'] for i in datos_entrenamiento]
  etiquetas = [i['etiqueta'] for i in datos_entrenamiento]

  return pd.DataFrame({'reclamo':reclamos, 'etiqueta':etiquetas})
"""
Lee un archivo JSON de frases y etiquetas y lo convierte en un DataFrame de Pandas.
Este archivo JSON se espera que contenga una lista de diccionarios, donde cada
diccionario tiene las claves 'reclamo' (para el texto) y 'etiqueta' (para la categoría).
    Args:
        direccion (str): La ruta completa al archivo JSON de entrada.

    Returns:
        pandas.DataFrame: Un DataFrame con dos columnas: 'reclamo' (texto del reclamo)
                          y 'etiqueta' (categoría del reclamo).
"""