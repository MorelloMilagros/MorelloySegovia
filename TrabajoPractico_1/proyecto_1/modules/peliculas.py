# módulo para organizar funciones o clases utilizadas en nuestro proyecto
# Crear tantos módulos como sea necesario para organizar el código
def cargar_peliculas(archivo='../data/frases_de_peliculas.txt'):
#Carga el archivo de frases y devuelve una lista de diccionarios {frase, pelicula}
    peliculas = []
    with open(archivo, 'r', encoding='utf-8') as f:
        for linea in f:
            if ';' in linea:
                frase, pelicula = linea.split(';', 1)
                peliculas.append({
                    'frase': frase.strip(),
                    'pelicula': pelicula.strip().title()  # Estandariza mayúsculas
                })
    return peliculas

def obtener_peliculas_unicas():
#Devuelve nombres de películas únicos y ordenados
    peliculas = cargar_peliculas()
    return sorted(list({p['pelicula'] for p in peliculas}))

def generar_trivia(num_preguntas):
#Genera preguntas aleatorias con opciones múltiples
    peliculas = cargar_peliculas()
    preguntas = random.sample(peliculas, num_preguntas)
    
    for p in preguntas:
        opciones = random.sample(
            [pel for pel in obtener_peliculas_unicas() if pel != p['pelicula']],
            2
        )
        opciones.append(p['pelicula'])
        random.shuffle(opciones)
        p['opciones'] = opciones
    
    return preguntas