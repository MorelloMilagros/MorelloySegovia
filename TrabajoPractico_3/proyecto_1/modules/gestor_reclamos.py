from modules.dominio import Reclamo
from modules.repositorio_abstracto import RepositorioAbstracto
from modules.monticulo_binario import MedianHeap
from datetime import datetime
class GestorDeReclamos:
    def __init__(self, repo: RepositorioAbstracto, clasificador=None):
        self.__repo=repo
        self.__numero_reclamos= len(self.__repo.obtener_todos_los_registros())
        self.__clasificador=clasificador
    @property
    def repo(self):
        return self.__repo 

    @property
    def numero_reclamos(self):
        return self.__numero_reclamos
    
    def agregar_nuevo_reclamo(self, descripcion, id_usuario, departamento):
        if not departamento:
            raise ValueError("El reclamo debe pertenecer a un departamento")
        reclamo= Reclamo(None, descripcion, "pendiente", id_usuario, departamento)
        self.__repo.guardar_registro(reclamo)

    def listar_reclamos(self):
        reclamos=self.__repo.obtener_todos_los_registros()
        resultado=[]
        for r in reclamos:
            r_dict= r.to_dict()
            r_dict['adherentes']= self.obtener_cantidad_adherentes(r.id)
            resultado.append(r_dict)
        return resultado

    def listar_reclamos_por_departamento(self, departamento):
        """Devuelve una lista de reclamos filtrados por departamento."""
        if not departamento:
            raise ValueError("El departamento no es válido")
        modelo_reclamos = self.__repo.obtener_todos_los_registros()
        reclamos_filtrados = [r for r in modelo_reclamos if r.departamento == departamento]
        
        return reclamos_filtrados

    def actualizar_estado_reclamo(self, id_reclamo, nuevo_estado):
        reclamo= self.__repo.obtener_registro_por_filtro("id", id_reclamo)
        if reclamo:
            reclamo.estado=nuevo_estado
            if nuevo_estado== "resuelto":
                reclamo.fecha_resolucion = datetime.utcnow()

            self.__repo.guardar_registro(reclamo)
        else:
            raise ValueError("El reclamo no existe")
        
    def eliminar_reclamo(self, id_reclamo):
        if self.__repo.obtener_registro_por_filtro("id", id_reclamo):
            self.__repo.eliminar_registro(id_reclamo)
        else:
            raise ValueError("El reclamo no existe")
        
    def adherir_a_reclamo(self, id_usuario, id_reclamo):
        self.__repo.adherir_usuario_a_reclamo(id_usuario,id_reclamo)

    def obtener_cantidad_adherentes(self, id_reclamo):
        return self.__repo.contar_adherentes(id_reclamo)
    
        
    def obtener_departamentos(self):
        """Devuelve una lista de los nombres de los departamentos con reclamos registrados."""
        modelo_reclamos = self.__repo.obtener_todos_los_registros()
        
        departamentos = {r.departamento for r in modelo_reclamos if r.departamento}  # 🔹 Usamos un conjunto para evitar duplicados
        
        return sorted(departamentos)  # 🔹 Ordenamos los nombres alfabéticamente

        
    def obtener_estadisticas(self, departamento):
        """Genera estadisticas de reclamos para un depto especifico"""
        reclamos= self.listar_reclamos_por_departamento(departamento)

        total=len(reclamos)
        pendientes= sum(1 for r in reclamos if r.estado == "pendiente")
        en_proceso = sum(1 for r in reclamos if r.estado== "en proceso")
        resueltos= sum(1 for r in reclamos if r. estado == "resuelto")
        #Inicio el monticulo binario
        median_heap_resueltos=MedianHeap()
        median_heap_en_proceso= MedianHeap()
        #Se insertan los tiempos de resolucion en la estructura
        for r in reclamos:
            tiempo_resolucion= r.calcular_tiempo_resolucion()
            if r.estado == "resuelto" and tiempo_resolucion is not None:
                median_heap_resueltos.insertar(tiempo_resolucion)
            elif r.estado== "en proceso" and tiempo_resolucion is not None:
                median_heap_en_proceso.insertar(tiempo_resolucion)

        mediana_resueltos= median_heap_resueltos.obtener_mediana() if resueltos > 0 else None
        mediana_en_proceso= median_heap_en_proceso.obtener_mediana() if en_proceso > 0 else None

        return {
            "total":total,
            "pendientes": pendientes,
            "en proceso": en_proceso,
            "mediana resueltos": mediana_resueltos,
            "mediana en proceso": mediana_en_proceso
        }
    
    def clasificar_descripcion(self, descripcion):
        if not self.__clasificador:
            raise ValueError("Clasificador no configurado")
        return self.__clasificador.clasificar([descripcion])[0]
    
    def buscar_similares(self, descripcion):
        categoria=  self.clasificar_descripcion(descripcion)
        todos= self.__repo.obtener_todos_los_registros()
        similares= [r for r in todos if self.clasificar_descripcion(r.descripcion)== categoria]
        return similares
    
