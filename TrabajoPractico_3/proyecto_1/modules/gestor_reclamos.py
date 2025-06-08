from modules.dominio import Reclamo
from modules.repositorio_abstracto import RepositorioAbstracto

class GestorDeReclamos:
    def __init__(self, repo: RepositorioAbstracto):
        self.__repo=repo
        self.__numero_reclamos= len(self.__repo.obtener_todos_los_registros())

    @property
    def numero_reclamos(self):
        return self.__numero_reclamos
    
    def agregar_nuevo_reclamo(self, descripcion, id_usuario):
        reclamo= Reclamo(None, descripcion, "pendiente", id_usuario)
        self.__repo.guardar_registro(reclamo)

    def listar_reclamos(self):
        return [reclamo.to_dict() for reclamo in self.__repo.obtener_todos_los_registros()]
    
    def actualizar_estado_reclamo(self, id_reclamo, nuevo_estado):
        reclamo= self.__repo.obtener_regristro_por_filtro("id", id_reclamo)
        if reclamo:
            reclamo.estado=nuevo_estado
            self.__repo.guardar_registro(reclamo)
        else:
            raise ValueError("El reclamo no existe")
        
    def eliminar_reclamo(self, id_reclamo):
        if self.__repo.obtener_registro_por_filtro("id", id_reclamo):
            self.__repo.eliminar_registro(id_reclamo)
        else:
            raise ValueError("El reclamo no existe")