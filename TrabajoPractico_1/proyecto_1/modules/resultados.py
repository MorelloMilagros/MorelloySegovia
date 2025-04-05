import json
from datetime import datetime
import matplotlib.pyplot as plt
import os
from pathlib import Path

class GestorResultados:
    def __init__(self, ruta_archivo):
        self.ruta_archivo = ruta_archivo
        self.datos = self._cargar_datos()
        self._crear_directorios()

    def _crear_directorios(self):
        """Crea los directorios necesarios si no existen"""
        Path('static/graficas').mkdir(parents=True, exist_ok=True)
        Path('static/pdf').mkdir(parents=True, exist_ok=True)

    def _cargar_datos(self):
        """Carga los datos existentes desde el archivo JSON"""
        try:
            if os.path.exists(self.ruta_archivo):
                with open(self.ruta_archivo, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return []
        except Exception as e:
            print(f"Error cargando datos: {e}")
            return []

    def guardar_resultado(self, usuario, aciertos, total):
        desaciertos=total-aciertos
        nuevo = {
            "usuario": usuario,
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "aciertos":aciertos,
            "desaciertos" : desaciertos ,
            "total":total,
            "resultado": f"{aciertos}/{total}"  
             
        }
        
        self.datos.append(nuevo)
        with open(self.ruta_archivo, 'w') as f:
            json.dump(self.datos, f, indent=4)
        
    def _preparar_historial(self):
        """Prepara los datos en el formato que necesitan tus funciones"""
        historial = []
        for dato in self.datos:
            historial.append((
                dato["usuario"],
                dato["fecha"],
                dato["aciertos"],
                dato["desaciertos"]
            ))
        return historial

    def generar_grafica_circular(self):
        """Versión adaptada de tu grafica_curvas"""
        historial = self._preparar_historial()
        if not historial:
            return None

        try:
            # Generar nombres únicos para los archivos
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            nombre_png = f"grafica_circular_{timestamp}.png"
            nombre_pdf = f"grafica_circular_{timestamp}.pdf"
            
            ruta_png = os.path.join('static', 'graficas', nombre_png)
            ruta_pdf = os.path.join('static', 'pdf', nombre_pdf)

            # Llamar a tu función original
            self.grafica_curvas(historial, ruta_png, ruta_pdf)
            
            return nombre_png
        except Exception as e:
            print(f"Error generando gráfica circular: {e}")
            return None

    def generar_grafica_evolucion(self):
        """Versión adaptada de tu grafica_prom"""
        historial = self._preparar_historial()
        if not historial:
            return None

        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            nombre_png = f"grafica_evolucion_{timestamp}.png"
            nombre_pdf = f"grafica_evolucion_{timestamp}.pdf"
            
            ruta_png = os.path.join('static', 'graficas', nombre_png)
            ruta_pdf = os.path.join('static', 'pdf', nombre_pdf)

            # Llamar a tu función original
            self.grafica_prom(historial, ruta_png, ruta_pdf)
            
            return nombre_png
        except Exception as e:
            print(f"Error generando gráfica de evolución: {e}")
            return None

    # Tus funciones originales adaptadas como métodos
    def grafica_curvas(self, historial2, ruta_png, ruta_pdf):
        fechas = []
        total_aciertos = 0
        total_desaciertos = 0
        
        for registro in historial2:
            fecha_str = registro[1].split(".")[0]  # Eliminar decimales de los segundos
            fecha = datetime.strptime(fecha_str, "%Y-%m-%d %H:%M:%S").date()
            fechas.append(fecha.strftime('%Y-%m-%d'))
            total_aciertos += int(registro[2])
            total_desaciertos += int(registro[3])

        # Crear el gráfico circular
        labels = ['Aciertos', 'Desaciertos']
        sizes = [total_aciertos, total_desaciertos]
        colors = ['lightgreen', 'lightcoral']
        explode = (0.1, 0)
        
        plt.figure(figsize=(6, 6))
        plt.pie(sizes, explode=explode, labels=labels, colors=colors, 
               autopct='%1.1f%%', startangle=140)
        plt.title('Porcentaje de Aciertos y Desaciertos acumulados')
        plt.axis('equal')
        
        # Guardar en ambos formatos
        plt.savefig(ruta_pdf)
        plt.savefig(ruta_png)
        plt.close()

    def grafica_prom(self, historial2, ruta_png, ruta_pdf):
        totales_por_fecha = {}
        
        for registro in historial2:
            fecha_str = registro[1].split()[0]  # Extraer solo la parte de la fecha
            fecha = datetime.strptime(fecha_str, "%Y-%m-%d").date()
            aciertos2 = int(registro[2])
            desaciertos2 = int(registro[3])
            
            if fecha in totales_por_fecha:
                totales_por_fecha[fecha]['aciertos'].append(aciertos2)
                totales_por_fecha[fecha]['desaciertos'].append(desaciertos2)
            else:
                totales_por_fecha[fecha] = {'aciertos': [aciertos2], 'desaciertos': [desaciertos2]}

        # Calcular promedios
        fechas2 = []
        promedio_aciertos = []
        promedio_desaciertos = []
        
        for fecha, totales in sorted(totales_por_fecha.items()):
            fechas2.append(fecha.strftime('%Y-%m-%d')) 
            promedio_aciertos.append(sum(totales['aciertos']))
            promedio_desaciertos.append(sum(totales['desaciertos']))

        # Graficar
        plt.figure(figsize=(8, 6))
        plt.plot(fechas2, promedio_aciertos, marker='o', label='Aciertos')
        plt.plot(fechas2, promedio_desaciertos, marker='x', label='Desaciertos')
        plt.title('Aciertos y Desaciertos por Fecha')
        plt.xlabel('Fecha')
        plt.ylabel('Cantidad')
        plt.xticks(rotation=45)
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        
        # Guardar en ambos formatos
        plt.savefig(ruta_pdf)
        plt.savefig(ruta_png)
        plt.close()