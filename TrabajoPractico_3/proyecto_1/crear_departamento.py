import sqlite3
import os
from datetime import datetime

# --- Configuración ---
# Ruta a la base de datos. Asegúrate de que coincida con la de tu proyecto.
DB_PATH = os.path.join("data", "base_datos.db")
# -------------------

def crear_nuevo_departamento():
    """
    Script de utilidad para dar de alta un nuevo departamento en el sistema.
    Lo hace creando un primer reclamo 'inicial' asociado a ese departamento.
    """
    print("--- Script para Crear Nuevo Departamento ---")

    # Verificar si la base de datos existe
    if not os.path.exists(DB_PATH):
        print(f"Error: No se encontró la base de datos en '{DB_PATH}'")
        return

    # Pedir el nombre del nuevo departamento al administrador
    nombre_dpto = input("Ingrese el nombre exacto del nuevo departamento: ").strip()

    if not nombre_dpto:
        print("Error: El nombre del departamento no puede estar vacío.")
        return

    try:
        # Conectar con la base de datos
        conexion = sqlite3.connect(DB_PATH)
        cursor = conexion.cursor()
        print("Conexión a la base de datos exitosa.")

        # 1. VERIFICAR SI EL DEPARTAMENTO YA EXISTE para no duplicarlo
        cursor.execute("SELECT 1 FROM reclamos WHERE departamento = ? LIMIT 1", (nombre_dpto,))
        if cursor.fetchone():
            print(f"Información: El departamento '{nombre_dpto}' ya existe en el sistema.")
            conexion.close()
            return
            
        # 2. BUSCAR UN USUARIO VÁLIDO PARA ASIGNARLE EL RECLAMO INICIAL
        #    Se busca un secretario técnico o, en su defecto, el primer usuario (ID=1).
        cursor.execute("SELECT id FROM usuarios WHERE rol = 'secretario' LIMIT 1")
        usuario_admin = cursor.fetchone()
        
        if not usuario_admin:
            # Si no hay secretario, usamos el usuario con ID 1 como fallback.
            cursor.execute("SELECT id FROM usuarios WHERE id = 1")
            usuario_admin = cursor.fetchone()

        if not usuario_admin:
            print("Error: No se encontró un usuario de sistema (secretario o ID=1) para asociar el reclamo inicial.")
            conexion.close()
            return
            
        id_usuario_sistema = usuario_admin[0]
        print(f"Usando ID de usuario del sistema: {id_usuario_sistema}")

        # 3. INSERTAR EL RECLAMO INICIAL para 'fundar' el departamento
        descripcion_inicial = f"Reclamo inicial para la creación del departamento '{nombre_dpto}'."
        estado_inicial = "pendiente"
        fecha_creacion = datetime.now()

        print(f"Intentando crear el departamento '{nombre_dpto}'...")
        cursor.execute(
            """
            INSERT INTO reclamos (descripcion, estado, departamento, fecha_creacion, id_usuario)
            VALUES (?, ?, ?, ?, ?)
            """,
            (descripcion_inicial, estado_inicial, nombre_dpto, fecha_creacion, id_usuario_sistema)
        )
        
        # Guardar cambios
        conexion.commit()
        
        print("\n¡ÉXITO!")
        print(f"El departamento '{nombre_dpto}' ha sido creado y ya está disponible en el sistema.")

    except sqlite3.Error as e:
        print(f"Ocurrió un error con la base de datos: {e}")
    finally:
        if 'conexion' in locals() and conexion:
            conexion.close()
            print("Conexión a la base de datos cerrada.")

if __name__ == "__main__":
    crear_nuevo_departamento()

#py crear_departamento.py