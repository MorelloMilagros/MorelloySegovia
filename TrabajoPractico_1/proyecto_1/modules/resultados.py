from modules.peliculas import cargar_peliculas, obtener_peliculas_unicas, generar_trivia
from modules.resultados import guardar_resultado, obtener_historial, generar_grafico_curvas

import json
import matplotlib.pyplot as plt
from datetime import datetime

def guardar_resultado(resultado, archivo='../data/resultados.json'):
    """Guarda los resultados en un archivo JSON"""
    with open(archivo, 'a') as f:
        f.write(json.dumps(resultado) + '\n')

def obtener_historial(archivo='../data/resultados.json'):
    """Carga el historial completo desde el archivo"""
    try:
        with open(archivo, 'r') as f:
            return [json.loads(linea) for linea in f]
    except FileNotFoundError:
        return []

def generar_grafico_curvas(historial):
    """Genera gráfico de aciertos por fecha"""
    fechas = [datetime.strptime(r['fecha'], "%d/%m/%Y %H:%M") for r in historial]
    aciertos = [r['aciertos'] for r in historial]

    plt.figure(figsize=(10, 5))
    plt.plot(fechas, aciertos, 'o-', label='Aciertos')
    plt.xlabel('Fecha')
    plt.ylabel('Aciertos')
    plt.title('Historial de Aciertos')
    plt.legend()
    plt.savefig('../static/grafico_curvas.png')
    plt.close()