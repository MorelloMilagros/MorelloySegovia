from modules.repositorio_concreto import RepositorioReclamosSQLAlchemy, RepositorioUsuariosSQLAlchemy
from modules.config import crear_engine

def crear_repositorio():
    session= crear_engine()
    repo_reclamos= RepositorioReclamosSQLAlchemy(session())
    repo_usuarios= RepositorioUsuariosSQLAlchemy(session())
    return repo_reclamos, repo_usuarios
