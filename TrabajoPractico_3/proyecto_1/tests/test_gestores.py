# tests/test_gestores.py
import unittest
from unittest.mock import MagicMock, patch
from modules.gestor_usuarios import GestorDeUsuarios
from modules.gestor_reclamos import GestorDeReclamos
from modules.dominio import Usuario, Reclamo
from datetime import datetime

class TestGestores(unittest.TestCase):

    def setUp(self):
        self.mock_repo_usuarios = MagicMock()
        self.mock_repo_reclamos = MagicMock()
        self.mock_clasificador = MagicMock()
        
        self.gestor_usuarios = GestorDeUsuarios(self.mock_repo_usuarios)
        self.gestor_reclamos = GestorDeReclamos(self.mock_repo_reclamos, self.mock_clasificador)

    # --- Pruebas GestorDeUsuarios ---
    def test_registrar_usuario_exitoso(self):
        self.mock_repo_usuarios.obtener_registro_por_filtro.return_value = None
        self.gestor_usuarios.registrar_nuevo_usuario("Maria", "Lopez", "marial", "maria@test.com", "pass123", "docente")
        self.mock_repo_usuarios.guardar_registro.assert_called_once()

    def test_registrar_usuario_email_duplicado_falla(self):
        self.mock_repo_usuarios.obtener_registro_por_filtro.return_value = MagicMock(spec=Usuario)
        with self.assertRaisesRegex(ValueError, "El usuario ya está registrado"):
            self.gestor_usuarios.registrar_nuevo_usuario("Maria", "Lopez", "marial", "maria@test.com", "pass123", "docente")

    def test_modificar_rol_usuario_no_existente_falla(self):
        self.mock_repo_usuarios.obtener_registro_por_filtro.return_value = None
        with self.assertRaisesRegex(ValueError, "El usuario no existe"):
            self.gestor_usuarios.modificar_rol(999, 'jefe')

    # --- Pruebas GestorDeReclamos ---
    def test_listar_reclamos_para_usuarios_solo_pendientes(self):
        # Arrange: Simulamos que el repo devuelve reclamos con distintos estados
        reclamo_pendiente = MagicMock(spec=Reclamo)
        reclamo_pendiente.to_dict.return_value = {'id': 1, 'estado': 'pendiente'}
        self.mock_repo_reclamos.obtener_registros_por_filtros.return_value = [reclamo_pendiente]
        
        # Act
        resultado = self.gestor_reclamos.listar_reclamos_para_usuarios()

        # Assert
        # Verificamos que se llamó al repo pidiendo explícitamente solo los pendientes
        self.mock_repo_reclamos.obtener_registros_por_filtros.assert_called_with(estado="pendiente")
        self.assertEqual(len(resultado), 1)

    def test_listar_reclamos_por_depto_y_estado(self):
        self.mock_repo_reclamos.obtener_registros_por_filtros.return_value = []
        self.gestor_reclamos.listar_reclamos_por_departamento("Soporte", "resuelto")
        self.mock_repo_reclamos.obtener_registros_por_filtros.assert_called_with(departamento="Soporte", estado="resuelto")

    def test_eliminar_reclamo_no_existente_falla(self):
        self.mock_repo_reclamos.obtener_registro_por_filtro.return_value = None
        with self.assertRaisesRegex(ValueError, "El reclamo no existe"):
            self.gestor_reclamos.eliminar_reclamo(999)

    def test_adherir_usuario_a_reclamo(self):
        self.gestor_reclamos.adherir_a_reclamo(1, 2)
        self.mock_repo_reclamos.adherir_usuario_a_reclamo.assert_called_once_with(1, 2)

    def test_clasificar_descripcion_sin_clasificador_falla(self):
        gestor_sin_clf = GestorDeReclamos(self.mock_repo_reclamos, None)
        with self.assertRaisesRegex(ValueError, "Clasificador no configurado"):
            gestor_sin_clf._clasificar_descripcion("test")
            
if __name__ == '__main__':
    unittest.main()