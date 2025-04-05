from flask import Flask, render_template, request, redirect, url_for
from modules.peliculas import GestorPeliculas
from modules.trivia import Trivia
from modules.resultados import GestorResultados
import os

app = Flask(__name__)
app.secret_key = 'clave_segura_para_flask_1234567890'

# Configuración de rutas
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RUTA_DATOS = os.path.join(BASE_DIR, 'data', 'frases_de_peliculas.txt')
RUTA_RESULTADOS = os.path.join(BASE_DIR, 'data', 'resultados.json')

# Inicialización
gestor_peliculas = GestorPeliculas(RUTA_DATOS)
gestor_peliculas.cargar_datos()
gestor_resultados = GestorResultados(RUTA_RESULTADOS)

# Estado del juego
juego_actual = {
    'trivia': None,
    'frase_actual': None,
    'correcta_actual': None
}

@app.route('/')
def inicio():
    return render_template('inicio.html')

@app.route('/iniciar', methods=['POST'])
def iniciar_juego():
    usuario = request.form['usuario']
    num_frases = int(request.form['num_frases'])
    
    trivia = Trivia(gestor_peliculas)
    trivia.iniciar_juego(usuario, num_frases)
    
    # Generar primera pregunta
    frase, correcta, opciones = trivia.generar_opciones()
    
    # Guardar estado del juego
    juego_actual['trivia'] = trivia
    juego_actual['frase_actual'] = frase
    juego_actual['correcta_actual'] = correcta
    juego_actual['opciones_actuales'] = opciones
    
    return render_template('juego.html',
                         frase=frase,
                         opciones=opciones,
                         aciertos=0,
                         total=num_frases)

@app.route('/verificar', methods=['POST'])
def verificar_respuesta():
    if not juego_actual['trivia']:
        return redirect(url_for('inicio'))
    
    trivia = juego_actual['trivia']
    respuesta = request.form.get('respuesta')
    correcta = juego_actual['correcta_actual']
    
    # Verificar respuesta
    if respuesta and respuesta.lower() == correcta.lower():
        trivia.aciertos += 1
    
    # Generar nueva pregunta
    frase, correcta, opciones = trivia.generar_opciones()
    
    # Verificar si el juego terminó
    if not frase or len(trivia.frases_usadas) > trivia.num_frases:
        # Guardar resultados
        gestor_resultados.guardar_resultado(
            trivia.usuario,
            trivia.aciertos,
            trivia.num_frases
        )
        return render_template('final.html',
                            usuario=trivia.usuario,
                            aciertos=trivia.aciertos,
                            total=trivia.num_frases)
    
    # Actualizar estado del juego
    juego_actual['frase_actual'] = frase
    juego_actual['correcta_actual'] = correcta
    juego_actual['opciones_actuales'] = opciones
    
    return render_template('juego.html',
                         frase=frase,
                         opciones=opciones,
                         aciertos=trivia.aciertos,
                         total=trivia.num_frases)

@app.route("/resultados")
def mostrar_resultados():
    """Muestra el historial de partidas"""
    return render_template("resultados.html", 
                         resultados=gestor_resultados.datos)

@app.route("/graficas")
def mostrar_graficas():
    grafica_circular = gestor_resultados.generar_grafica_circular()
    grafica_lineal = gestor_resultados.generar_grafica_evolucion()

    return render_template("graficas.html",grafica_circular=grafica_circular, grafica_lineal=grafica_lineal,resultados=gestor_resultados.datos[-10:])
if __name__ == '__main__':
    app.run(debug=True)