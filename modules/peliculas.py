import os
import random

class GestorPeliculas:
    def __init__(self, ruta_archivo):
        self.ruta_archivo = os.path.normpath(ruta_archivo)  # Normaliza rutas para Windows/Linux
        self.frases = []
        self.peliculas = set()
        self._cargado = False  # Flag para controlar carga

    def cargar_datos(self):
        if not os.path.exists(self.ruta_archivo):
            raise FileNotFoundError(f"Archivo no encontrado: {self.ruta_archivo}")
        
        with open(self.ruta_archivo, 'r', encoding='utf-8') as f:
            for linea in f:
                if ';' not in linea:
                    continue
                frase, pelicula = linea.strip().split(';', 1)
                self.frases.append((frase, pelicula.strip()))
                self.peliculas.add(pelicula.strip().lower())
        self._cargado = True

    def obtener_peliculas_ordenadas(self):
        if not self._cargado:
            self.cargar_datos()
        return sorted(self.peliculas)

    def obtener_frase_aleatoria(self, excluir=None):
        if not self._cargado:
            self.cargar_datos()
        excluir = excluir or []
        disponibles = [f for f in self.frases if f not in excluir]
        return random.choice(disponibles) if disponibles else None