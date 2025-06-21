from modules.graficador_abstracto import Graficador
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import io

# Desactiva el modo interactivo de Matplotlib para que funcione en un entorno de servidor
plt.switch_backend('Agg')

class GraficadorMatplotlib(Graficador):
    """
    Implementación concreta de Graficador que utiliza Matplotlib y WordCloud para
    generar las visualizaciones.
    """

    def _guardar_grafico_en_buffer(self) -> bytes:
        """Función de ayuda para guardar la figura actual en un buffer de memoria."""
        buf = io.BytesIO()
        # bbox_inches='tight' asegura que no se corten las etiquetas
        plt.savefig(buf, format='png', bbox_inches='tight')
        buf.seek(0)
        plt.close()  # Es crucial cerrar la figura para liberar memoria
        return buf.read()

    def crear_grafico_barras(self, datos: dict, titulo: str, etiqueta_x: str, etiqueta_y: str) -> bytes:
        labels = list(datos.keys())
        values = list(datos.values())

        fig, ax = plt.subplots(figsize=(8, 5))
        ax.bar(labels, values, color=['#FF9999', '#66B2FF', '#99FF99', '#FFCC99'])
        ax.set_ylabel(etiqueta_y)
        ax.set_xlabel(etiqueta_x)
        ax.set_title(titulo, fontsize=16)
        
        # Añadir los valores numéricos encima de cada barra
        for i, v in enumerate(values):
            ax.text(i, v + 0.1, str(v), ha='center', fontweight='bold')
            
        return self._guardar_grafico_en_buffer()

    def crear_grafico_torta(self, datos: dict, titulo: str) -> bytes:
        # Filtra datos con valor 0 para no mostrarlos en el gráfico
        labels_filtrados = [label for label, value in datos.items() if value > 0]
        values_filtrados = [value for value in datos.values() if value > 0]

        if not values_filtrados:
            return None # No se puede generar un gráfico sin datos

        fig, ax = plt.subplots(figsize=(8, 8))
        ax.pie(values_filtrados, labels=labels_filtrados, autopct='%1.1f%%', startangle=90,
               colors=['#FF9999', '#66B2FF', '#99FF99', '#FFCC99'])
        ax.axis('equal')  # Asegura que el gráfico sea un círculo perfecto
        ax.set_title(titulo, fontsize=16)
        
        return self._guardar_grafico_en_buffer()

    def crear_nube_palabras(self, palabras_frecuentes: list, titulo: str) -> bytes:
        if not palabras_frecuentes:
            return None

        # El generador espera un diccionario de frecuencias
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(dict(palabras_frecuentes))

        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title(titulo, fontsize=16)

        return self._guardar_grafico_en_buffer()