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
        Path('static/graficas').mkdir(parents=True, exist_ok=True)
        Path('static/pdf').mkdir(parents=True, exist_ok=True)

    def _cargar_datos(self):
        try:
            if os.path.exists(self.ruta_archivo):
                with open(self.ruta_archivo, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return []
        except Exception as e:
            print(f"Error cargando datos: {e}")
            return []

    def guardar_resultado(self, usuario, aciertos, total):
        try:
            nuevo = {
                "usuario": usuario,
                "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "aciertos": aciertos,
                "desaciertos": total - aciertos,
                "total": total,
                "resultado": f"{aciertos}/{total}"
            }
            
            self.datos.append(nuevo)
            with open(self.ruta_archivo, 'w', encoding='utf-8') as f:
                json.dump(self.datos, f, indent=4)
    
        except Exception as e:
            print(f"Error guardando resultado: {e}")

    def _preparar_historial(self):
        historial = []
        for dato in self.datos:
            try:
            # Validación completa de campos
                if all(key in dato for key in ['usuario', 'fecha', 'aciertos', 'desaciertos']):
                    historial.append((
                        dato["usuario"],
                        dato["fecha"],
                        int(dato["aciertos"]),
                        int(dato["desaciertos"])
                    ))
            except (KeyError, ValueError) as e:
                print(f"Registro corrupto omitido: {dato}. Error: {str(e)}")
        return historial

    # ========== CORRECCIONES APLICADAS AQUÍ ==========
    def generar_grafica_circular(self):
        #Genera gráfica circular y devuelve el nombre del archivo PNG
        try:
            historial = self._preparar_historial()
            if not historial:
                return "grafica_vacia.png"
            
            # Nombres fijos para que server.py los encuentre
            nombre_png = f"grafica_circular.png"
            nombre_pdf = f"Graficocircular.pdf"

            # Rutas completas
            ruta_png = os.path.join('static', 'graficas', nombre_png)
            ruta_pdf = os.path.join('static', 'pdf', nombre_pdf)
            # Generar gráfica
            self.grafica_curvas(historial, ruta_png, ruta_pdf)
            return nombre_png
            
        except Exception as e:
            print(f"Error generando gráfica circular: {e}")
            return None

    def generar_grafica_evolucion(self):
        #Genera gráfica de evolución y devuelve el nombre del archivo PNG
        try:
            historial = self._preparar_historial()
            if not historial:
                return None
            #Nombres fijos
            nombre_png = f"grafica_evolucion.png"
            nombre_pdf = f"Grafico1.pdf"
            #Rutas completas    
            ruta_png = os.path.join('static', 'graficas', nombre_png)
            ruta_pdf = os.path.join('static', 'pdf', nombre_pdf)
            #Generar grafica
            self.grafica_prom(historial, ruta_png, ruta_pdf)
            return nombre_png
            
        except Exception as e:
            print(f"Error generando gráfica de evolución: {e}")
            return None
  

    def grafica_curvas(self, historial2, ruta_png, ruta_pdf):
        # Mantener método original sin cambios
        fechas = []
        total_aciertos = 0
        total_desaciertos = 0
        
        for registro in historial2:
            fecha_str = registro[1].split(".")[0]
            fecha = datetime.strptime(fecha_str, "%Y-%m-%d %H:%M:%S").date()
            fechas.append(fecha.strftime('%Y-%m-%d'))
            total_aciertos += int(registro[2])
            total_desaciertos += int(registro[3])

        labels = ['Aciertos', 'Desaciertos']
        sizes = [total_aciertos, total_desaciertos]
        colors = ['lightgreen', 'lightcoral']
        explode = (0.1, 0)
        
        plt.figure(figsize=(6, 6))
        plt.pie(sizes, explode=explode, labels=labels, colors=colors, 
               autopct='%1.1f%%', startangle=140)
        plt.title('Porcentaje de Aciertos y Desaciertos acumulados')
        plt.axis('equal')
        
        plt.savefig(ruta_pdf)
        plt.savefig(ruta_png)
        plt.close()

    def grafica_prom(self, historial2, ruta_png, ruta_pdf):
        # Mantener método original sin cambios
        totales_por_fecha = {}
        
        for registro in historial2:
            fecha_str = registro[1].split()[0]
            fecha = datetime.strptime(fecha_str, "%Y-%m-%d").date()
            aciertos2 = int(registro[2])
            desaciertos2 = int(registro[3])
            
            if fecha in totales_por_fecha:
                totales_por_fecha[fecha]['aciertos'].append(aciertos2)
                totales_por_fecha[fecha]['desaciertos'].append(desaciertos2)
            else:
                totales_por_fecha[fecha] = {'aciertos': [aciertos2], 'desaciertos': [desaciertos2]}

        fechas2 = []
        promedio_aciertos = []
        promedio_desaciertos = []
        
        for fecha, totales in sorted(totales_por_fecha.items()):
            fechas2.append(fecha.strftime('%Y-%m-%d')) 
            promedio_aciertos.append(sum(totales['aciertos']))
            promedio_desaciertos.append(sum(totales['desaciertos']))

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
        
        plt.savefig(ruta_pdf)
        plt.savefig(ruta_png)
        plt.close()