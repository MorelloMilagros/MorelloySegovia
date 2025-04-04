import random

class Trivia:
    def __init__(self, gestor_peliculas):
        self.gestor = gestor_peliculas
        self.frases_usadas = []
        self.aciertos = 0
        self.usuario = ""
        self.num_frases = 0

    def iniciar_juego(self, usuario, num_frases):
        self.usuario = usuario
        self.num_frases = num_frases
        self.frases_usadas = []
        self.aciertos = 0

    def generar_opciones(self):
        while True:
            frase, correcta = self.gestor.obtener_frase_aleatoria(self.frases_usadas)
            if not frase:
                return None, None, None
            self.frases_usadas.append((frase, correcta))
            opciones = [correcta]
            peliculas = list(self.gestor.peliculas)
            while len(opciones) < 3:
                opcion = random.choice(peliculas)
                if opcion != correcta.lower() and opcion not in opciones:
                    opciones.append(opcion)
            random.shuffle(opciones)
            return frase, correcta, opciones

    def verificar_respuesta(self, respuesta, correcta):
        if respuesta.lower() == correcta.lower():
            self.aciertos += 1
            return True
        return False