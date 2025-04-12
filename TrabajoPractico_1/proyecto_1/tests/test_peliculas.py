import os
from modules.peliculas import GestorPeliculas

# Ruta ABSOLUTA CORREGIDA (cambia según tu estructura real)
ruta_archivo = r"data\frases_de_peliculas.txt"

# Debug
print(f"Buscando archivo en: {ruta_archivo}")
print(f"¿Existe el archivo?: {'SÍ' if os.path.exists(ruta_archivo) else 'NO'}")

try:
    gestor = GestorPeliculas(ruta_archivo)
    gestor.cargar_datos()
    print("\n¡Datos cargados correctamente!")
    print("Películas disponibles:", gestor.obtener_peliculas_ordenadas())
    frase, pelicula = gestor.obtener_frase_aleatoria()
    print(f"Frase aleatoria: '{frase}' (de {pelicula})")
except Exception as e:
    print(f"\nERROR: {type(e).__name__}: {e}")