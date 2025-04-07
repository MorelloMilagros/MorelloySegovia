from flask import Flask

app = Flask(__name__, static_folder='static')  # Usar __name__ es más estándar
app.secret_key = 'clave_secreta_123'  # Añade la clave secreta aquí