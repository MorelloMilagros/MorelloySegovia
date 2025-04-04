import random
ruta_archivo = "TrabajoPractico_1\proyecto_1\data\frases_de_peliculas.txt"


class GestorPeliculas:
    def __init__(self, ruta_archivo):
        self.ruta_archivo = ruta_archivo
        self.frases = []
        self.peliculas = set()

    def cargar_datos(self):
        with open(self.ruta_archivo, 'r', encoding='utf-8') as f:
            for linea in f:
                frase, pelicula = linea.strip().split(';')
                self.frases.append((frase, pelicula.strip()))
                self.peliculas.add(pelicula.strip().lower())

    def obtener_peliculas_ordenadas(self):
        return sorted(self.peliculas)

    def obtener_frase_aleatoria(self, excluir=None):
        excluir = excluir or []
        disponibles = [f for f in self.frases if f not in excluir]
        return random.choice(disponibles) if disponibles else None