from flask import Flask, render_template, request, redirect, url_for, send_file
from modules.peliculas import GestorPeliculas
from modules.trivia import Trivia
from modules.resultados import GestorResultados
from modules.pdf import descargar_pdf
import os
from PyPDF4 import PdfFileMerger
# ... (imports y config inicial)

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
    'correcta_actual': None,
    'opciones_actuales':None
    }
# Ruta principal: Muestra el formulario de inicio
@app.route('/')
def inicio():
    return render_template('inicio.html')
# Procesa el formulario de inicio y crea nueva trivia
#retorna el render del template "inicio.html"
@app.route('/iniciar', methods=['POST'])
def iniciar_juego():
    #Inicia nueva partida de trivia y genera la primera pregunta
    """Recibe nombre de  usuario cantidad de preguntas
    Retorna la renderizacion del template "juego.html" con la primera pregunta"""
    usuario = request.form['usuario']
    num_frases = int(request.form['num_frases'])
    
    trivia = Trivia(gestor_peliculas)
    trivia.iniciar_juego(usuario, num_frases)
    
    # Generar primera pregunta y guarda estado en variable global
    frase, correcta, opciones = trivia.generar_opciones()
    print("*"*100)
    print(frase)
    print(correcta)
    print(opciones)
    print("*"*100)

    
    # Guardar estado del juego
    juego_actual['trivia'] = trivia # Persistencia entre requests
    juego_actual['frase_actual'] = frase
    juego_actual['correcta_actual'] = correcta
    juego_actual['opciones_actuales'] = opciones #Falta definicion en diccionario
    
    return render_template('juego.html',
                         frase=frase,
                         opciones=opciones,
                         aciertos=0,
                         total=num_frases)

# Verifica respuesta y genera nueva pregunta o termina
@app.route('/verificar', methods=['POST'])
def verificar_respuesta():
    #Verifica la respuesta del usuario y genera una nueva pregunta o finaliza el juego 
    """ Analiza si la respuesta es correcta y suma el acierto. Luego genera otra pegunta o finaliza el juego
    Retorna: template "juego.html" o "final.html"""
  
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
    #Muestra las graficas lineal y circular
    """Retorna el render del template "graficas.html" """
    grafica_circular = gestor_resultados.generar_grafica_circular()
    grafica_lineal = gestor_resultados.generar_grafica_evolucion()

    return render_template("graficas.html",grafica_circular=grafica_circular, grafica_lineal=grafica_lineal, resultados=gestor_resultados.datos)
@app.route ("/peliculas")

def mostrar_peliculas():
    #Muestra la lista de peliculas almacenadas
    """Retorna el rende dle template "peliculas.html" """
    peliculas= gestor_peliculas.obtener_peliculas_ordenadas()
    return render_template("peliculas.html",peliculas=peliculas)


@app.route("/descargar")

def descargar():
    # Permite la descarga de un archivo PDF con gráficas
    """retorna un archivo pdf con las graficas del sistema"""
    return descargar_pdf()
        
if __name__ == '__main__':
    app.run(debug=True)
