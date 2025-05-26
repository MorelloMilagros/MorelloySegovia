import os
import random

# Normaliza rutas para compatibilidad entre SO (Windows/Linux/macOS)
class GestorPeliculas:
    def __init__(self, ruta_archivo):
        #Inicializa el gestor de películas con la ruta del archivo de datos.
        """ Args:
            ruta_archivo (str): Ruta del archivo que contiene frases y películas.
        """
        self.ruta_archivo = os.path.normpath(ruta_archivo)  # Normaliza rutas para Windows/Linux
        self.frases = [] # Almacena tuplas (frase, película)
        self.peliculas = set() # Usa un set para evitar duplicados automáticamente
        self._cargado = False  # Bandera para evitar carga múltiple del archivo

    def cargar_datos(self):
        #Carga las frases y películas desde el archivo de datos
        # Validación básica: ¿Existe el archivo?
        """ Raises:
            FileNotFoundError: Si el archivo de datos no existe."""
        if not os.path.exists(self.ruta_archivo):
            raise FileNotFoundError(f"Archivo no encontrado: {self.ruta_archivo}")
        
        
        # Procesamiento línea por línea con encoding UTF-8 (soporta acentos)
        with open(self.ruta_archivo, 'r', encoding='utf-8') as f:
            for linea in f:   # Ignora líneas mal formateadas
                if ';' not in linea:
                    continue
                    # Split en el primer ';' por si la frase contiene ';'
                frase, pelicula = linea.strip().split(';', 1)
                self.frases.append((frase, pelicula.strip()))
                 # Lowercase para normalizar nombres (evitar "Matrix" vs "matrix")
                self.peliculas.add(pelicula.strip().lower())
        self._cargado = True  # Marca como cargado


    def obtener_peliculas_ordenadas(self):
        #Obtiene la lista ordenada de películas disponibles. Carga datos si es que no lo estan
        """ Returns:
            list: Lista de nombres de películas ordenadas alfabéticamente"""
        if not self._cargado: # Carga bajo demanda (lazy loading)
            self.cargar_datos()
                    # Convierte el set a lista ordenada alfabéticamente
        return sorted(self.peliculas)

    def obtener_frase_aleatoria(self, excluir=None):
        #Obtiene una frase aletoria de todas las disponbles, excluye ya usadas.
        """Args:
            excluir (list, optional): Lista de frases ya utilizadas (tuplas de frase y película). 
            Si es None, no excluye ninguna frase
        
        Retorna: tuple / None: Una tupla (frase, película) aleatoria, o None si no hay frases disponibles
        """
        if not self._cargado:
            self.cargar_datos()
        excluir = excluir or [] # Manejo de valor por defecto mutable
        # Filtra frases no usadas (excluir es lista de tuplas (frase, pelicula))
        disponibles = [f for f in self.frases if f not in excluir]
        # Retorna None si no hay frases disponibles (evita error)
        return random.choice(disponibles) if disponibles else None