# tests/test_dominio.py
import pytest
from datetime import datetime, timedelta
from modules.dominio import Usuario, Reclamo

# --- Pruebas para la clase Usuario ---

def test_crear_usuario_ok():
    """Verifica que un usuario se cree correctamente con datos válidos."""
    usuario = Usuario(1, "Juan", "Perez", "juanp", "juan@test.com", "pass123", "usuario", "Soporte técnico", "estudiante")
    assert usuario.id == 1
    assert usuario.nombre == "Juan"
    assert usuario.email == "juan@test.com"
    assert usuario.rol == "usuario"
    assert usuario.es_jefe() is False
    assert usuario.es_secretario() is False

def test_crear_jefe_ok():
    """Verifica los métodos de rol para un jefe."""
    jefe = Usuario(2, "Ana", "Gomez", "anag", "ana@test.com", "pass123", "jefe", "Soporte técnico", "docente")
    assert jefe.es_jefe() is True
    assert jefe.get_id() == "2"

def test_crear_usuario_nombre_vacio_falla():
    """Verifica que no se pueda crear un usuario con nombre vacío."""
    with pytest.raises(ValueError, match="El nombre del usuario debe ser un string y no debe estar vacío"):
        Usuario(1, " ", "Perez", "juanp", "juan@test.com", "pass123", "usuario", "Soporte técnico", "estudiante")

# --- Pruebas para la clase Reclamo ---

def test_crear_reclamo_ok():
    """Verifica que un reclamo se cree correctamente."""
    fecha_creacion = datetime.now()
    reclamo = Reclamo(1, "El proyector no funciona", "pendiente", 1, "Soporte técnico", fecha_creacion)
    assert reclamo.id == 1
    assert reclamo.descripcion == "El proyector no funciona"
    assert reclamo.estado == "pendiente"
    assert reclamo.fecha_creacion == fecha_creacion

def test_crear_reclamo_sin_fecha_asigna_fecha_actual():
    """Verifica que si no se pasa fecha de creación, se asigna la actual."""
    reclamo = Reclamo(1, "Test de fecha", "pendiente", 1, "Soporte técnico")
    assert reclamo.fecha_creacion is not None
    assert isinstance(reclamo.fecha_creacion, datetime)

def test_reclamo_estado_invalido_falla():
    """Verifica que no se pueda crear un reclamo con un estado inválido."""
    with pytest.raises(ValueError, match="El estado debe ser 'pendiente', 'resuelto', 'en proceso' o 'invalido'"):
        Reclamo(1, "Test estado", "estado_raro", 1, "Soporte técnico")

def test_calcular_tiempo_resolucion():
    """Verifica que el cálculo de días de resolución sea correcto."""
    fecha_creacion = datetime.now()
    fecha_resolucion = fecha_creacion + timedelta(days=5)
    reclamo = Reclamo(1, "Test de tiempo", "resuelto", 1, "Soporte técnico", fecha_creacion, p_fecha_resolucion=fecha_resolucion)
    assert reclamo.calcular_tiempo_resolucion() == 5

def test_calcular_tiempo_resolucion_sin_fechas_es_none():
    """Verifica que si faltan fechas, el tiempo de resolución sea None."""
    reclamo = Reclamo(1, "Test sin fechas", "pendiente", 1, "Soporte técnico")
    assert reclamo.calcular_tiempo_resolucion() is None
    