from modules.repositorio_concreto import RepositorioReclamosSQLAlchemy, RepositorioUsuariosSQLAlchemy
from modules.config import crear_engine

def crear_repositorio():
    session= crear_engine()
    repo_reclamos= RepositorioReclamosSQLAlchemy(session())
    repo_usuarios= RepositorioUsuariosSQLAlchemy(session())
    return repo_reclamos, repo_usuarios
"""
    Función factoría para crear y retornar instancias de los repositorios.

    Utiliza la función `crear_engine` del módulo `config` para obtener una sesión
    de SQLAlchemy, y luego crea instancias de `RepositorioReclamosSQLAlchemy`
    y `RepositorioUsuariosSQLAlchemy`, pasándoles la sesión.

    Este enfoque centraliza la creación de repositorios y permite un fácil
    cambio de la implementación de la base de datos en el futuro.

    Returns:
        tuple: Una tupla que contiene (repositorio_reclamos, repositorio_usuarios).
               Cada elemento es una instancia de su respectivo repositorio concreto.
"""