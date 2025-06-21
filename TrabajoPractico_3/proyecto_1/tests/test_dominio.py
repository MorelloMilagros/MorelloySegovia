# tests/test_dominio.py
import unittest
from datetime import datetime, timedelta
from modules.dominio import Usuario, Reclamo

class TestDominio(unittest.TestCase):

    def test_crear_usuario_ok(self):
        """Prueba la creación exitosa de un usuario con datos válidos."""
        # Arrange
        usuario = Usuario(1, "Juan", "Perez", "juanp", "juan@test.com", "pass123", "usuario", "Soporte", "estudiante")
        
        # Act & Assert
        self.assertEqual(usuario.id, 1)
        self.assertEqual(usuario.nombre, "Juan")
        self.assertEqual(usuario.rol, "usuario")
        self.assertFalse(usuario.es_jefe())
        self.assertTrue(usuario.is_active)
        self.assertEqual(usuario.get_id(), "1")

    def test_crear_jefe_ok(self):
        """Prueba los métodos de rol para un jefe."""
        # Arrange
        jefe = Usuario(2, "Ana", "Gomez", "anag", "ana@test.com", "pass123", "jefe", "Soporte", "docente")
        
        # Act & Assert
        self.assertTrue(jefe.es_jefe())
        self.assertFalse(jefe.es_secretario())

    def test_crear_usuario_nombre_vacio_falla(self):
        """Prueba que no se puede crear un usuario con nombre vacío."""
        # Arrange, Act & Assert
        with self.assertRaisesRegex(ValueError, "El nombre del usuario debe ser un string y no debe estar vacío"):
            Usuario(1, " ", "Perez", "juanp", "juan@test.com", "pass123", "usuario", "Soporte", "estudiante")

    def test_crear_reclamo_ok(self):
        """Prueba la creación exitosa de un reclamo."""
        # Arrange
        fecha = datetime.now()
        reclamo = Reclamo(p_id=1, p_descripcion="Proyector quemado", p_estado="pendiente", pd_id_usuario=1, p_departamento="Soporte", p_fecha_creacion=fecha)
        
        # Act & Assert
        self.assertEqual(reclamo.id, 1)
        self.assertEqual(reclamo.descripcion, "Proyector quemado")
        self.assertEqual(reclamo.estado, "pendiente")
        self.assertEqual(reclamo.fecha_creacion, fecha)
        self.assertIn("Proyector quemado", str(reclamo))

    def test_reclamo_estado_invalido_falla(self):
        """Prueba que un estado inválido lanza un error."""
        with self.assertRaises(ValueError):
            Reclamo(1, "Test", "estado_raro", 1, "Depto")
            
    def test_calcular_tiempo_resolucion(self):
        """Verifica que el cálculo de días de resolución sea correcto."""
        # Arrange
        fecha_creacion = datetime.now()
        fecha_resolucion = fecha_creacion + timedelta(days=5)
        reclamo = Reclamo(1, "Test", "resuelto", 1, "Soporte", fecha_creacion, p_fecha_resolucion=fecha_resolucion)
        
        # Act
        tiempo = reclamo.calcular_tiempo_resolucion()
        
        # Assert
        self.assertEqual(tiempo, 5)

    def test_calcular_tiempo_resolucion_sin_fechas_es_none(self):
        """Verifica que si faltan fechas, el tiempo de resolución sea None."""
        # Arrange
        reclamo = Reclamo(1, "Test", "pendiente", 1, "Soporte")
        
        # Act & Assert
        self.assertIsNone(reclamo.calcular_tiempo_resolucion())

if __name__ == '__main__':
    unittest.main()