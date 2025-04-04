from flask import Flask, render_template, request, session, redirect, url_for
from modules.peliculas import GestorPeliculas
from modules.trivia import Trivia
from modules.resultados import GestorResultados
import os

# Configuración de Flask
app = Flask(__name__, static_folder="static")
app.secret_key = "clave_super_secreta_123!"  # ¡Cambia esta clave!

# Inicializar módulos
gestor_peliculas = GestorPeliculas("data/frases_de_peliculas.txt")
gestor_peliculas.cargar_datos()
gestor_resultados = GestorResultados("data/resultados.json")

# -------------------- Rutas --------------------
@app.route("/")
def inicio():
    """Muestra la página principal con el formulario de inicio"""
    return render_template("inicio.html")

@app.route("/iniciar", methods=["POST"])
def iniciar_juego():
    """Inicia una nueva partida"""
    session.clear()
    session["usuario"] = request.form["usuario"]
    session["num_frases"] = int(request.form["num_frases"])
    session["aciertos"] = 0
    session["frases_usadas"] = []
    return redirect(url_for("juego"))

@app.route("/juego")
def juego():
    """Muestra una pregunta de la trivia"""
    if len(session.get("frases_usadas", [])) >= session["num_frases"]:
        return redirect(url_for("finalizar"))

    trivia = Trivia(gestor_peliculas)
    frase, correcta, opciones = trivia.generar_opciones()
    
    if not frase:  # Si no hay más frases disponibles
        return redirect(url_for("finalizar"))
    
    session["frase_actual"] = frase
    session["correcta_actual"] = correcta
    session["opciones_actuales"] = opciones
    session["frases_usadas"].append((frase, correcta))
    
    return render_template("juego.html", 
                         frase=frase, 
                         opciones=opciones,
                         aciertos=session["aciertos"],
                         total=session["num_frases"])

@app.route("/verificar", methods=["POST"])
def verificar_respuesta():
    """Verifica si la respuesta del usuario es correcta"""
    respuesta = request.form.get("pelicula", "").strip().lower()
    correcta = session["correcta_actual"].lower()
    
    if respuesta == correcta:
        session["aciertos"] += 1
    
    if len(session["frases_usadas"]) < session["num_frases"]:
        return redirect(url_for("juego"))
    else:
        return redirect(url_for("finalizar"))

@app.route("/finalizar")
def finalizar():
    """Muestra los resultados finales y guarda el historial"""
    gestor_resultados.guardar_resultado(
        session["usuario"],
        session["aciertos"],
        session["num_frases"]
    )
    return render_template("final.html",
                         aciertos=session["aciertos"],
                         total=session["num_frases"])

@app.route("/peliculas")
def listar_peliculas():
    """Muestra el listado de todas las películas"""
    peliculas = gestor_peliculas.obtener_peliculas_ordenadas()
    return render_template("peliculas.html", peliculas=peliculas)

@app.route("/resultados")
def mostrar_resultados():
    """Muestra el historial de partidas"""
    return render_template("resultados.html", 
                         resultados=gestor_resultados.datos)

@app.route("/graficas")
def generar_graficas():
    """Genera y muestra las gráficas"""
    gestor_resultados.generar_grafica("lineal")
    gestor_resultados.generar_grafica("circular")
    return render_template("graficas.html")

# -------------------- Ejecutar la app --------------------
if __name__ == "__main__":
    app.run(debug=True)