# tests/test_server.py
import unittest
from unittest.mock import patch, MagicMock
from server import app

class TestServer(unittest.TestCase):

    def setUp(self):
        """Configura el cliente de prueba de Flask para cada test."""
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'test-secret-key' # Usar una clave diferente para tests
        app.config['WTF_CSRF_ENABLED'] = False
        self.client = app.test_client()

    def _login(self, client, email='test@user.com', rol='usuario', departamento='Soporte'):
        """Función de ayuda para simular un login dentro de un contexto de cliente."""
        usuario_dict = {'id': 99, 'nombre': 'Test', 'email': email, 'password': 'hash', 'rol': rol, 'departamento': departamento}
        
        with patch('server.gestor_usuarios.autenticar_usuario', return_value=usuario_dict):
            return client.post('/login', data={'email': email, 'password': 'password'}, follow_redirects=True)

    def test_pagina_inicio_publica(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Bienvenido al Sistema de Reclamos", response.data)

    def test_registro_exitoso(self):
        with patch('server.gestor_usuarios.registrar_nuevo_usuario') as mock_registro:
            mock_registro.return_value = None
            response = self.client.post('/register', data={
                'nombre': 'Test', 'apellido': 'User', 'username': 'testuser',
                'email': 'test@example.com', 'password': 'password123',
                'confirmacion': 'password123', 'claustro': 'estudiante'
            }, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Usuario registrado exitosamente", response.data)

    def test_login_y_acceso_a_menu_principal(self):
        """Prueba que un usuario normal puede loguearse y ver su menú."""
        with self.client as c:
            response = self._login(c, rol='usuario')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Men\xc3\xba Principal", response.data)

    def test_acceso_a_dashboard_como_jefe(self):
        """Prueba que un jefe puede loguearse y ver el dashboard."""
        with self.client as c, \
             patch('server.gestor_reclamos.listar_reclamos_por_departamento', return_value=[]), \
             patch('server.gestor_reclamos.obtener_estadisticas', return_value={}):
            
            self._login(c, rol='jefe')
            response = c.get('/dashboard')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Panel de Administraci\xc3\xb3n", response.data)

    def test_acceso_denegado_a_dashboard_para_usuario_normal(self):
        """Prueba que un usuario normal es redirigido del dashboard."""
        with self.client as c, patch('server.current_user') as mock_current_user:
            self._login(c, rol='usuario')
            
            # Configuramos el mock de current_user para la segunda petición
            mock_current_user.es_jefe.return_value = False
            mock_current_user.es_secretario.return_value = False

            response = c.get('/dashboard', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Acceso denegado", response.data)

    def test_crear_reclamo_con_datos_faltantes(self):
        """Prueba que el form de reclamo valida los datos."""
        with self.client as c:
            self._login(c)
            response = c.post('/agregar_reclamo', data={}, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Faltan datos", response.data)

    def test_logout_exitoso(self):
        """Prueba que el logout funciona y limpia la sesión."""
        with self.client as c:
            self._login(c)
            response = c.get('/logout', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Bienvenido al Sistema de Reclamos", response.data)
            
            # Verificamos que ya no podemos acceder a una página protegida
            response_after_logout = c.get('/mis_reclamos', follow_redirects=True)
            self.assertIn(b"Please log in to access this page", response_after_logout.data)

    def test_generar_reporte_html(self):
        """Prueba la generación de reportes en HTML para un jefe."""
        with self.client as c, \
             patch('server.gestor_reclamos.listar_reclamos_por_departamento', return_value=[]), \
             patch('server.gestor_reclamos.obtener_estadisticas', return_value={}):
            self._login(c, rol='jefe')
            response = c.get('/generar_reporte?formato=html')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Reporte de Estado de Reclamos", response.data)

if __name__ == '__main__':
    unittest.main()