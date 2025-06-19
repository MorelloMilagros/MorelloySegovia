from abc import ABC, abstractmethod

class RepositorioAbstracto(ABC):
    """
    Clase base abstracta para todos los repositorios de datos.

    Define la interfaz (contrato) que cualquier repositorio concreto debe implementar.
    Esto asegura que la lógica de negocio (en los gestores) dependa de una abstracción
    en lugar de una implementación concreta de la base de datos, lo que facilita
    el cambio de la tecnología de persistencia en el futuro.

    Métodos abstractos que deben ser implementados por las subclases:
    - `guardar_registro`: Guarda una nueva entidad.
    - `obtener_todos_los_registros`: Recupera todas las entidades.
    - `modificar_registro`: Actualiza una entidad existente.
    - `obtener_registro_por_filtro`: Busca una entidad por un filtro específico.
    - `eliminar_registro`: Elimina una entidad por su ID.
    """
    @abstractmethod
    def guardar_registro(self, entidad):
        """
        Guarda una nueva entidad en el repositorio.

        Args:
            entidad: El objeto de dominio (ej. Usuario, Reclamo) a guardar.
        """
        raise NotImplementedError("Debe implementar el método 'guardar_registro'")

    @abstractmethod
    def obtener_todos_los_registros(self) -> list:
        """
        Obtiene una lista de todas las entidades del repositorio.

        Returns:
            list: Una lista de objetos de dominio.
        """
        raise NotImplementedError("Debe implementar el método 'obtener_todos_los_registros'")
    
    @abstractmethod
    def modificar_registro(self, entidad_modificada):
        """
        Modifica una entidad existente en el repositorio.

        Args:
            entidad_modificada: El objeto de dominio con los datos actualizados.
        """
        raise NotImplementedError("Debe implementar el método 'modificar_registro'")    
    
    @abstractmethod
    def obtener_registro_por_filtro(self, filtro, valor):
        """
        Obtiene un único registro del repositorio basándose en un filtro.

        Args:
            filtro (str): El nombre del atributo por el cual filtrar (ej. "id", "email").
            valor: El valor a buscar para el filtro.

        Returns:
            any or None: El objeto de dominio si se encuentra, de lo contrario, None.
        """
        raise NotImplementedError("Debe implementar el método 'obtener_registro_por_filtro'")
    
    @abstractmethod
    def eliminar_registro(self, id):
        """
        Elimina un registro del repositorio por su identificador.

        Args:
            id: El identificador del registro a eliminar.
        """
        raise NotImplementedError("Debe implementar el método 'eliminar_registro'")