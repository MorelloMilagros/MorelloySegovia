# modules/gestor_reclamos.py
from modules.dominio import Reclamo
from modules.repositorio_abstracto import RepositorioAbstracto
from datetime import datetime, timedelta
class GestorDeReclamos:
    """
    Clase que encapsula la lógica de negocio para la gestión de reclamos.

    Actúa como una capa de servicio entre la interfaz de usuario y el repositorio
    de datos, aplicando reglas de negocio y coordinando operaciones.

    Atributos:
        __repo (RepositorioAbstracto): Una instancia del repositorio de reclamos
                                      para interactuar con la persistencia.
        __numero_reclamos (int): El número total de reclamos en el sistema.
                                 (Nota: este atributo podría no estar siempre actualizado
                                 si los reclamos se añaden/eliminan frecuentemente
                                 sin recalcularlo).
        __clasificador (ClaimsClassifier, opcional): Una instancia del clasificador
                                                    de texto para categorizar reclamos.
    """
    def __init__(self, repo: RepositorioAbstracto, clasificador=None):
        """
        Inicializa el GestorDeReclamos.

        Args:
            repo (RepositorioAbstracto): La implementación del repositorio a utilizar.
            clasificador (ClaimsClassifier, opcional): El clasificador de texto de reclamos.
        """
        self.__repo = repo
        # Se obtiene el número inicial de reclamos. Considerar si esto debe ser dinámico.
        self.__numero_reclamos = len(self.__repo.obtener_todos_los_registros()) 
        self.__clasificador = clasificador

    @property
    def repo(self):
        """Obtiene la instancia del repositorio asociada al gestor."""
        return self.__repo

    @property
    def numero_reclamos(self):
        """
        Obtiene el número actual de reclamos.

        Nota: Este valor se inicializa al crear el gestor y no se actualiza
              automáticamente con cada nueva adición/eliminación.
              Para un conteo exacto, se debería consultar el repositorio.
        """
        return self.__numero_reclamos

    def agregar_nuevo_reclamo(self, descripcion, id_usuario, departamento, p_foto=None):
        """
        Agrega un nuevo reclamo al sistema.

        Crea un objeto Reclamo con estado "pendiente" y la fecha de creación actual,
        y lo persiste a través del repositorio.

        Args:
            descripcion (str): La descripción del reclamo.
            id_usuario (int): El ID del usuario que crea el reclamo.
            departamento (str): El departamento al que se asigna el reclamo.
            p_foto (str, opcional): El nombre del archivo de la foto adjunta.

        Raises:
            ValueError: Si el departamento no es válido (vacío o solo espacios).
        """
        if not departamento or departamento.strip() == "":
            raise ValueError("El reclamo debe pertenecer a un departamento")
            
        reclamo = Reclamo(None, descripcion, "pendiente", id_usuario, departamento, p_foto=p_foto)
        self.__repo.guardar_registro(reclamo)


    def listar_reclamos(self):
        """
        Lista todos los reclamos registrados con su cantidad de adherentes.

        Returns:
            list: Una lista de diccionarios, donde cada diccionario representa un reclamo
                  e incluye un campo 'adherentes' con la cantidad de usuarios adheridos.
        """
        reclamos = self.__repo.obtener_registros_por_filtros() # Asume que sin filtros trae todo
        resultado = []
        for r in reclamos:
            r_dict = r.to_dict()
            r_dict['adherentes'] = self._obtener_cantidad_adherentes(r.id)
            resultado.append(r_dict)
        return resultado

    # En modules/gestor_reclamos.py

    def listar_reclamos_por_departamento(self, departamento, estado=None):
        """
        Lista reclamos (como OBJETOS) filtrados por departamento y opcionalmente por estado.
        """
        if not departamento or departamento.strip() == "":
            raise ValueError("El departamento no es válido")

        filtros = {"departamento": departamento.strip()}
        if estado:
            filtros["estado"] = estado

        # El repositorio ya devuelve una lista de objetos Reclamo, simplemente la retornamos.
        reclamos_objetos = self.__repo.obtener_registros_por_filtros(**filtros)
        return reclamos_objetos

    def listar_reclamos_para_usuarios(self):
        """
        Obtiene solo los reclamos con estado 'pendiente', para la vista del usuario final.

        Returns:
            list: Una lista de diccionarios de reclamos en estado "pendiente",
                  incluyendo la cantidad de adherentes.
        """
        reclamos = self.__repo.obtener_registros_por_filtros(estado="pendiente")
        resultado = []
        for r in reclamos:
            r_dict = r.to_dict()
            r_dict['adherentes'] = self._obtener_cantidad_adherentes(r.id)
            resultado.append(r_dict)
        return resultado

    def actualizar_estado_reclamo(self, id_reclamo, nuevo_estado, dias_resolucion=None):
        """
        Actualiza el estado de un reclamo y, si pasa a "en proceso", asigna un tiempo de resolución.

        Args:
            id_reclamo (int): El ID del reclamo a actualizar.
            nuevo_estado (str): El nuevo estado para el reclamo
                                ("pendiente", "en proceso", "resuelto", "inválido").
            dias_resolucion (int, opcional): El número de días estimados para la resolución,
                                             requerido si `nuevo_estado` es "en proceso".

        Raises:
            ValueError: Si el reclamo no existe, si el nuevo estado es "en proceso"
                        y `dias_resolucion` es nulo o fuera del rango (1-15).
        """
        reclamo = self.repo.obtener_registro_por_filtro("id", id_reclamo)
        if not reclamo:
            raise ValueError("El reclamo no existe")

        reclamo.estado = nuevo_estado # La validación del estado se hace en el setter de la clase Reclamo
        
        if nuevo_estado == "resuelto":
            reclamo.fecha_resolucion = datetime.now()
        elif nuevo_estado == "en proceso":
            if dias_resolucion is None:
                raise ValueError("Para poner un reclamo 'en proceso', se debe especificar un tiempo de resolución.")
                
            try:
                dias_int = int(dias_resolucion)
                if not (1 <= dias_int <= 15):
                    raise ValueError("El tiempo de resolución debe estar entre 1 y 15 días.")
                reclamo.fecha_resolucion = datetime.now() + timedelta(days=dias_int)
            except (TypeError, ValueError):
                raise ValueError("El tiempo de resolución debe ser un número entero válido.")
        # Para "pendiente" o "inválido", la fecha_resolucion puede quedar como estaba o en None.
        # La lógica actual no la resetea a None si se vuelve de "en proceso" a "pendiente",
        # lo cual podría ser una consideración de diseño.
            
        self.repo.modificar_registro(reclamo)

    def eliminar_reclamo(self, id_reclamo):
        """
        Elimina un reclamo del sistema por su ID.

        Args:
            id_reclamo (int): El ID del reclamo a eliminar.

        Raises:
            ValueError: Si el reclamo con el ID especificado no existe.
        """
        if self.__repo.obtener_registro_por_filtro("id", id_reclamo):
            self.__repo.eliminar_registro(id_reclamo)
        else:
            raise ValueError("El reclamo no existe")

    def adherir_a_reclamo(self, id_usuario, id_reclamo):
        """
        Permite a un usuario adherirse a un reclamo existente.

        Args:
            id_usuario (int): El ID del usuario que desea adherirse.
            id_reclamo (int): El ID del reclamo al que adherirse.

        Raises:
            ValueError: Si el usuario ya está adherido a ese reclamo.
        """
        self.__repo.adherir_usuario_a_reclamo(id_usuario, id_reclamo)

    def _obtener_cantidad_adherentes(self, id_reclamo):
        """
        Obtiene la cantidad de usuarios adheridos a un reclamo específico.

        Args:
            id_reclamo (int): El ID del reclamo.

        Returns:
            int: El número de adherentes para el reclamo.
        """
        return self.__repo.contar_adherentes(id_reclamo)

    def obtener_departamentos(self):
        """
        Obtiene una lista de todos los departamentos únicos a los que se han asignado reclamos.

        Returns:
            list: Una lista ordenada alfabéticamente de los nombres de los departamentos.
        """
        modelo_reclamos = self.__repo.obtener_todos_los_registros()
        # Usamos un conjunto para almacenar departamentos únicos y luego lo convertimos a lista ordenada
        departamentos = {r.departamento for r in modelo_reclamos if r.departamento} 
        return sorted(departamentos)
        
    def obtener_reclamo(self, id_reclamo):
        """
        Obtiene un reclamo específico por su ID.

        Args:
            id_reclamo (int): El ID del reclamo a buscar.

        Returns:
            Reclamo or None: El objeto Reclamo si se encuentra, de lo contrario, None.
        """
        return self.__repo.obtener_registro_por_filtro("id", id_reclamo)

    def _clasificar_descripcion(self, descripcion):
        """
        Clasifica una descripción de reclamo en una categoría.

        Utiliza el clasificador de aprendizaje automático configurado en el gestor.

        Args:
            descripcion (str): El texto del reclamo a clasificar.

        Returns:
            str: La categoría predicha para el reclamo.

        Raises:
            ValueError: Si el clasificador no ha sido configurado en el gestor.
        """
        if not self.__clasificador:
            raise ValueError("Clasificador no configurado")
        # El método clasificar del ClaimsClassifier espera una lista, y devuelve una lista,
        # por lo que tomamos el primer elemento [0]
        return self.__clasificador.clasificar([descripcion])[0]

    def buscar_similares(self, descripcion):
        """
        Busca reclamos similares a una descripción dada.

        Primero clasifica la descripción para obtener su categoría, luego
        busca todos los reclamos existentes que pertenecen a esa misma categoría.

        Args:
            descripcion (str): La descripción del nuevo reclamo a comparar.

        Returns:
            list: Una lista de objetos Reclamo que son similares (misma categoría).
        """
        categoria = self._clasificar_descripcion(descripcion)
        todos_reclamos = self.__repo.obtener_todos_los_registros()
        # Filtra los reclamos cuya descripción, al ser clasificada, cae en la misma categoría
        similares = [r for r in todos_reclamos if self._clasificar_descripcion(r.descripcion) == categoria]
        return similares

    def derivar_reclamo(self, id_reclamo, nuevo_departamento):
        """
        Cambia el departamento de un reclamo específico.
        Utilizado por la Secretaría Técnica.
        """
        reclamo = self.repo.obtener_registro_por_filtro("id", id_reclamo)
        if not reclamo:
            raise ValueError("El reclamo a derivar no existe.")
        
        if not nuevo_departamento or nuevo_departamento == reclamo.departamento:
            raise ValueError("Debe seleccionar un departamento diferente para derivar.")

        reclamo.departamento = nuevo_departamento
        self.repo.modificar_registro(reclamo)
