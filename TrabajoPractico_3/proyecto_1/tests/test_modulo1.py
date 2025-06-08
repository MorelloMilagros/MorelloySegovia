# Archivo de test para realizar pruebas unitarias del modulo1
from modules.data_manager import DataManager

# Inicializar el manejador de datos
data_manager = DataManager()

# Probar guardar datos
reclamos_prueba = [
    {"id": 1, "texto": "El servicio no funciona", "tipo": "urgente"},
    {"id": 2, "texto": "No recibí el pedido", "tipo": "normal"}
]
data_manager.guardar_reclamos(reclamos_prueba)

# Probar cargar datos
reclamos = data_manager.cargar_reclamos()
print("Reclamos guardados correctamente:", reclamos)
