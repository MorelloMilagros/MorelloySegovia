import json
from datetime import datetime
import matplotlib.pyplot as plt
import os

class GestorResultados:
    def __init__(self, ruta_archivo):
        self.ruta_archivo = ruta_archivo
        self.datos = self._cargar_datos()

    def _cargar_datos(self):
        try:
            with open(self.ruta_archivo, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def guardar_resultado(self, usuario, aciertos, total):
        nuevo = {
            "usuario": usuario,
            "fecha": datetime.now().strftime("%d/%m/%y %H:%M"),
            "resultado": f"{aciertos}/{total}"
        }
        self.datos.append(nuevo)
        with open(self.ruta_archivo, 'w') as f:
            json.dump(self.datos, f, indent=4)

    def generar_grafica(self, tipo="lineal"):
        if not os.path.exists('static/graficas'):
            os.makedirs('static/graficas')
        fechas = [datetime.strptime(d["fecha"], "%d/%m/%y %H:%M") for d in self.datos]
        aciertos = [int(d["resultado"].split('/')[0]) for d in self.datos]
        desaciertos = [int(d["resultado"].split('/')[1]) - aciertos[i] for i, d in enumerate(self.datos)]
        
        plt.figure()
        if tipo == "lineal":
            plt.plot(fechas, aciertos, label="Aciertos")
            plt.plot(fechas, desaciertos, label="Desaciertos")
            plt.xticks(rotation=45)
        elif tipo == "circular":
            plt.pie([sum(aciertos), sum(desaciertos)], labels=["Aciertos", "Desaciertos"], autopct='%1.1f%%')
        
        nombre_archivo = f"grafica_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
        ruta = os.path.join('static', 'graficas', nombre_archivo)
        plt.savefig(ruta, bbox_inches='tight')
        plt.close()
        return nombre_archivo