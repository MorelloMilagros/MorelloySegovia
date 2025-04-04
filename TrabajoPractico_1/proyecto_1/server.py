# Ejemplo de aplicación principal en Flask
from flask import Flask,  render_template, redirect, request , url_for, flash
import json
from modules.config import app
import os
import datetime

# Configuración explícita de rutas
app = Flask(__name__,
            static_folder=os.path.join(os.path.dirname(__file__), 'static'),
            template_folder=os.path.join(os.path.dirname(__file__), 'templates'))

# Página de inicio
@app.route('/')
def index():
    return render_template('inicio.html')

@app.route('/iniciar', methods=['POST'])
def iniciar_trivia():
    nombre= request.form.get('nombre')
    num_frases= int(request.form.get('frases'))
#Validaciones
    if not nombre or num_frases < 3 or num_frases > 15:
        flash("Nombre o número de frases inválido")
        return redirect(url_for('inicio'))


@app.route('/listar')
def ver_peliculas():
    pass

@app.route('/ver_historial')
def ver_historial():
    pass

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)