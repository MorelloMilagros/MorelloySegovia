# tests/test_server.py
import unittest
from unittest.mock import patch

# Importamos la app directamente desde el archivo 'server' para asegurar
# que estamos probando la instancia correcta con todas las rutas registradas.
from server import app
from modules.dominio import Reclamo # Importamos Reclamo para usarlo en mocks

class TestServer(unittest.TestCase):

    def setUp(self):
        """Configura el entorno de pruebas antes de cada test."""
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'test-secret-key'
        app.config['WTF_CSRF_ENABLED'] = False
        self.client = app.test_client()

    def _login(self, rol='usuario', user_id=99, departamento='Soporte'):
        """
        Función de ayuda para simular un usuario logueado.
        Parchea la capa más baja posible (el gestor de usuarios) para permitir
        que la lógica del GestorDeLogin se ejecute de forma normal.
        """
        user_data = {
            'id': user_id,
            'nombre': 'Usuario de Prueba',
            'email': 'test@example.com',
            'password': 'hashed_password_mock',
            'rol': rol,
            'departamento': departamento,
            'claustro': 'estudiante'
        }

        # Interceptamos la llamada a la base de datos y devolvemos nuestro usuario falso.
        patcher = patch('modules.gestor_usuarios.GestorDeUsuarios.cargar_usuario', return_value=user_data)
        
        self.patcher = patcher.start()
        self.addCleanup(self.patcher.stop)

        # Simulamos la sesión del navegador para que Flask-Login encuentre el user_id.
        with self.client.session_transaction() as sess:
            sess['_user_id'] = user_id
            sess['user_id'] = user_id

    def test_pagina_inicio_publica(self):
        """Verifica que la página de inicio carga correctamente."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Bienvenido al Sistema de Reclamos", response.data)

    def test_registro_exitoso(self):
        """Prueba que un usuario puede registrarse y es redirigido."""
        with patch('modules.gestor_usuarios.GestorDeUsuarios.registrar_nuevo_usuario', return_value=None):
            response = self.client.post('/register', data={
                'nombre': 'Test', 'apellido': 'User', 'username': 'testuser',
                'email': 'test@example.com', 'password': 'password123',
                'confirmacion': 'password123', 'claustro': 'estudiante'
            }, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Usuario registrado exitosamente", response.data)

    def test_acceso_a_dashboard_como_jefe(self):
        """Verifica que un usuario con rol 'jefe' puede acceder al dashboard."""
        with patch('modules.analitica.Analitica.obtener_datos_dashboard', return_value=([], {})) as mock_dashboard_data:
            self._login(rol='jefe', departamento='Mantenimiento')
            response = self.client.get('/dashboard')
            
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Panel de Administraci\xc3\xb3n", response.data)
            mock_dashboard_data.assert_called_once_with(departamento='Mantenimiento')

    def test_acceso_denegado_a_dashboard_para_usuario_normal(self):
        """Verifica que un usuario normal es redirigido del dashboard."""
        self._login(rol='usuario')
        response = self.client.get('/dashboard', follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        # que es el comportamiento esperado tras la redirección.
        self.assertIn(b"Bienvenido, Usuario de Prueba", response.data)

    def test_generar_reporte_html_como_jefe(self):
        """Prueba que un jefe puede generar un reporte HTML."""
        with patch('modules.analitica.Analitica.generar_reporte_formateado') as mock_reporte:
            mock_reporte.return_value = ("<html><body>Reporte de Prueba</body></html>", "text/html", {})
            
            self._login(rol='jefe', departamento='Soporte')
            response = self.client.get('/generar_reporte?formato=html')
            
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Reporte de Prueba", response.data)
            self.assertEqual(response.mimetype, 'text/html')
            mock_reporte.assert_called_with('Soporte', 'html')

    def test_derivar_reclamo_como_secretario(self):
        """
        NUEVA PRUEBA: Verifica que un secretario puede derivar un reclamo.
        """
        with patch('modules.gestor_reclamos.GestorDeReclamos.obtener_reclamo') as mock_obtener, \
             patch('modules.gestor_reclamos.GestorDeReclamos.derivar_reclamo') as mock_derivar, \
             patch('modules.gestor_reclamos.GestorDeReclamos.obtener_departamentos', return_value=['Mantenimiento']):
            
            mock_obtener.return_value = Reclamo(p_id=1, p_descripcion="Test", p_estado="pendiente", 
                                                pd_id_usuario=1, p_departamento="Soporte técnico")

            self._login(rol='secretario', departamento='Secretaría Técnica')
            
            response = self.client.post('/derivar/1', data={
                'nuevo_departamento': 'Mantenimiento'
            }, follow_redirects=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Reclamo 1 derivado exitosamente a Mantenimiento.", response.data)
            mock_derivar.assert_called_once_with(1, 'Mantenimiento')

if __name__ == '__main__':
    unittest.main()
