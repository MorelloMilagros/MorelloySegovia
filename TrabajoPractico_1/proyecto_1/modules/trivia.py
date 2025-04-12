import random

class Trivia:
    def __init__(self, gestor_peliculas):
        self.gestor = gestor_peliculas # Inyección de dependencia
        self.frases_usadas = [] # Evita repeticiones de frases
        self.aciertos = 0
        self.usuario = ""
        self.num_frases = 0

    def iniciar_juego(self, usuario, num_frases):
           # Reinicia estado para nueva partida
        self.usuario = usuario
        self.num_frases = num_frases
        self.frases_usadas = []
        self.aciertos = 0

    def generar_opciones(self):
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
        # Comparación case-insensitive
        if respuesta.lower() == correcta.lower():
            self.aciertos += 1
            return True
        return False