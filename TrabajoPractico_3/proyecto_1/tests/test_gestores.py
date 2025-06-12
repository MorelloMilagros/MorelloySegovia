# tests/test_gestores.py
import pytest
from unittest.mock import MagicMock
from modules.gestor_usuarios import GestorDeUsuarios
from modules.gestor_reclamos import GestorDeReclamos
from modules.dominio import Usuario, Reclamo
from datetime import datetime

# --- Pruebas para GestorDeUsuarios ---

@pytest.fixture
def mock_repo_usuarios(mocker):
    """Crea un 'doble de riesgo' para el repositorio de usuarios."""
    return mocker.MagicMock()

@pytest.fixture
def gestor_usuarios(mock_repo_usuarios):
    """Crea una instancia del gestor de usuarios con el repo falso."""
    return GestorDeUsuarios(mock_repo_usuarios)

def test_registrar_usuario_nuevo_ok(gestor_usuarios, mock_repo_usuarios):
    """Verifica el registro exitoso de un usuario que no existe."""
    mock_repo_usuarios.obtener_registro_por_filtro.return_value = None
    gestor_usuarios.registrar_nuevo_usuario("Maria", "Lopez", "marial", "maria@test.com", "pass123", "docente")
    mock_repo_usuarios.guardar_registro.assert_called_once()
    args, _ = mock_repo_usuarios.guardar_registro.call_args
    assert args[0].nombre == "Maria"

def test_registrar_usuario_duplicado_falla(gestor_usuarios, mock_repo_usuarios):
    """Verifica que no se pueda registrar un email que ya existe."""
    mock_repo_usuarios.obtener_registro_por_filtro.return_value = Usuario(2, "Maria", "Gomez", "marial", "maria@test.com", "pass123", "docente", "Académica", "docente")
    
    # --- LÍNEA CORREGIDA ---
    # Ahora la prueba espera el mensaje de error exacto que tu código produce.
    with pytest.raises(ValueError, match="El usuario ya está registrado, por favor inicie sesion."):
        gestor_usuarios.registrar_nuevo_usuario("Otra", "Maria", "otramaria", "maria@test.com", "pass456", "docente")

# --- Pruebas para GestorDeReclamos ---

@pytest.fixture
def mock_repo_reclamos(mocker):
    """Crea un 'doble de riesgo' para el repositorio de reclamos."""
    return mocker.MagicMock()

@pytest.fixture
def gestor_reclamos(mock_repo_reclamos, mocker):
    """Crea una instancia del gestor de reclamos con el repo y clasificador falsos."""
    mock_clasificador = mocker.MagicMock()
    return GestorDeReclamos(mock_repo_reclamos, mock_clasificador)

def test_agregar_reclamo_ok(gestor_reclamos, mock_repo_reclamos):
    """Verifica que se pueda agregar un reclamo correctamente."""
    gestor_reclamos.agregar_nuevo_reclamo("La calefacción no anda", 1, "Mantenimiento")
    mock_repo_reclamos.guardar_registro.assert_called_once()
    args, _ = mock_repo_reclamos.guardar_registro.call_args
    assert args[0].descripcion == "La calefacción no anda"

def test_agregar_reclamo_sin_depto_falla(gestor_reclamos):
    """Verifica que un reclamo deba tener un departamento."""
    with pytest.raises(ValueError, match="El reclamo debe pertenecer a un departamento"):
        gestor_reclamos.agregar_nuevo_reclamo("Sin depto", 1, "")

def test_actualizar_estado_a_en_proceso_ok(gestor_reclamos, mock_repo_reclamos):
    """Verifica que se pueda actualizar el estado a 'en proceso' con días válidos."""
    reclamo_original = Reclamo(1, "Test", "pendiente", 1, "Soporte técnico", p_fecha_creacion=datetime.now())
    mock_repo_reclamos.obtener_registro_por_filtro.return_value = reclamo_original
    gestor_reclamos.actualizar_estado_reclamo(1, "en proceso", dias_resolucion=5)
    mock_repo_reclamos.modificar_registro.assert_called_once()
    reclamo_modificado = mock_repo_reclamos.modificar_registro.call_args[0][0]
    assert reclamo_modificado.estado == "en proceso"

def test_actualizar_estado_en_proceso_sin_dias_falla(gestor_reclamos, mock_repo_reclamos):
    """Verifica que falle si se pasa a 'en proceso' sin días."""
    reclamo_original = Reclamo(1, "Test", "pendiente", 1, "Soporte técnico")
    mock_repo_reclamos.obtener_registro_por_filtro.return_value = reclamo_original
    with pytest.raises(ValueError, match="Para poner un reclamo 'en proceso', se debe especificar un tiempo de resolución."):
        gestor_reclamos.actualizar_estado_reclamo(1, "en proceso", dias_resolucion=None)

def test_obtener_estadisticas_completo(gestor_reclamos, mock_repo_reclamos):
    """Verifica que el cálculo de estadísticas sea correcto."""
    lista_reclamos = [
        Reclamo(1, "wifi lento", "resuelto", 1, "Soporte técnico", datetime(2025, 6, 1), p_fecha_resolucion=datetime(2025, 6, 5)), # 4 días
        Reclamo(2, "proyector quemado", "pendiente", 2, "Soporte técnico", datetime(2025, 6, 10)),
        Reclamo(3, "no hay tiza", "pendiente", 1, "Soporte técnico", datetime(2025, 6, 11))
    ]
    mock_repo_reclamos.obtener_registros_por_filtros.return_value = lista_reclamos
    
    stats = gestor_reclamos.obtener_estadisticas("Soporte técnico")
    
    assert stats["total"] == 3
    assert stats["pendientes"] == 2
    assert stats["mediana resueltos"] == 4.0