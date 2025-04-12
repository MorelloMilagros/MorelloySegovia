from flask import Flask
# Configuración base de Flask: 
# - __name__ para resolver rutas de recursos
# - static_folder para servir archivos estáticos (CSS, JS, imágenes)
# - secret_key para manejar sesiones y mensajes flash (seguridad básica)
app = Flask(__name__, static_folder='static')  
app.secret_key = 'clave_secreta_123'   # Clave necesaria para operaciones de sesión