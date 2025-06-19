from flask import Flask
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask_login import LoginManager
import datetime
from modules.modelos import Base

app = Flask("ReclamosAPI")
app.config['SECRET_KEY']= 'clave_12332141'

URL_BD= 'sqlite:///data/base_datos.db'

def crear_engine():
    engine= create_engine(URL_BD)
    Base.metadata.create_all(engine)
    Session= sessionmaker(bind=engine)
    return Session
"""
Crea y configura el motor de la base de datos SQLAlchemy.
Inicializa la conexión con la base de datos SQLite definida en `URL_BD`.
Se asegura de que todas las tablas (definidas en `modules.modelos.Base.metadata`)
existan en la base de datos. Si no existen, las crea.
Finalmente, retorna una clase `Session` configurada para interactuar con la base de datos.
Returns:
sqlalchemy.orm.sessionmaker: Una clase Sessionmaker configurada.
"""
app.config.from_object(__name__)
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_FILE_DIR"] = "./flask_session_cache"
app.config["SESSION_PERMANENT"] = False
app.config["PERMANENT_SESSION_LIFETIME"] = datetime.timedelta(minutes=10)  # Sesión un poco más larga
Session(app)

login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
