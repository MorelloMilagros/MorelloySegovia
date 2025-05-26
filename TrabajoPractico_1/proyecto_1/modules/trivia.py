import random

class Trivia:
    def __init__(self, gestor_peliculas):
        #Inicializa la instancia de Trivia con un gestor de películas.
        """Args:
            gestor_peliculas (GestorPeliculas): Instancia de `GestorPeliculas` para obtener frases.
        """
        self.gestor = gestor_peliculas # Inyección de dependencia
        self.frases_usadas = [] # Evita repeticiones de frases
        self.aciertos = 0
        self.usuario = ""
        self.num_frases = 0

    def iniciar_juego(self, usuario, num_frases):
       #Reinicia el estado del juego y establece el usuario y número de frases.
        """Args:
            usuario (str): Nombre del usuario que jugará la trivia.
            num_frases (int): Número de frases a utilizar en la partida.
        """
        self.usuario = usuario
        self.num_frases = num_frases
        self.frases_usadas = []
        self.aciertos = 0

    def generar_opciones(self):
        #Genera una pregunta con opciones de respuesta.
        """Busca una frase aleatoria y crea una lista de opciones con una respuesta correcta 
        y dos opciones incorrectas.
        
        Retorna: tuple: Una tupla con (frase, respuesta correcta, lista de opciones),
                   o (None, None, None) si no hay más frases disponibles.
        """
        while True: # Busca hasta tener 3 opciones válidas
            frase, correcta = self.gestor.obtener_frase_aleatoria(self.frases_usadas)
            if not frase:
                return None, None, None # Caso sin frases disponibles
            self.frases_usadas.append((frase, correcta))
            opciones = [correcta]
            peliculas = list(self.gestor.peliculas)
         # Genera 2 opciones incorrectas únicas

            while len(opciones) < 3:       
                opcion = random.choice(peliculas)
                if opcion != correcta.lower() and opcion not in opciones:
                    opciones.append(opcion)
            random.shuffle(opciones) # Mezcla para no dar pistas
            return frase, correcta, opciones

    def verificar_respuesta(self, respuesta, correcta):
        #Verifica si la respuesta dada por el usuario es correcta.
        """Args:
            respuesta (str): Respuesta elegida por el usuario.
            correcta (str): Respuesta correcta esperada.
        
        Retorna: bool: "True" si la respuesta es correcta, "False" en caso contrario.
        """
        # Comparación case-insensitive
        if respuesta.lower() == correcta.lower():
            self.aciertos += 1
            return True
        return False


if __name__== "__main__":
    from modules.peliculas import GestorPeliculas
    RUTA_DATOS = "C:\program_avanzada\MorelloySegovia\TrabajoPractico_1\proyecto_1\modules\data\frases_de_peliculas.txt"
    g=GestorPeliculas(RUTA_DATOS)
    t= Trivia(g)
    print(t.generar_opciones())
