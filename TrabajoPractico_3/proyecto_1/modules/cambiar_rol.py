import sqlite3
import os

# --- Configuración ---
# Define el nombre de usuario y el nuevo rol aquí
USERNAME_A_MODIFICAR = "Mili"
NUEVO_ROL = "secretario"
# También puedes definir el departamento si quieres cambiarlo al mismo tiempo
NUEVO_DEPARTAMENTO = "Soporte técnico"
# -------------------


# Construye la ruta a la base de datos con el nombre correcto
db_path = os.path.join("data", "base_datos.db")

# Verificar si la base de datos existe
if not os.path.exists(db_path):
    print(f"Error: No se encontró la base de datos en la ruta '{db_path}'")
else:
    try:
        # Conectar con la base de datos
        conexion = sqlite3.connect(db_path)
        cursor = conexion.cursor()

        print(f"Intentando cambiar el rol de '{USERNAME_A_MODIFICAR}' a '{NUEVO_ROL}'...")

        # Ejecutar la actualización
        cursor.execute(
            "UPDATE usuarios SET rol = ?, departamento = ? WHERE username = ?",
            (NUEVO_ROL, NUEVO_DEPARTAMENTO, USERNAME_A_MODIFICAR)
        )

        # Verificar si se modificó alguna fila
        if cursor.rowcount == 0:
            print(f"Error: No se encontró ningún usuario con el username '{USERNAME_A_MODIFICAR}'. No se realizaron cambios.")
        else:
            # Guardar cambios y cerrar conexión
            conexion.commit()
            print(f"¡Éxito! El rol de '{USERNAME_A_MODIFICAR}' ha sido actualizado a '{NUEVO_ROL}'.")

    except sqlite3.Error as e:
        print(f"Ocurrió un error con la base de datos: {e}")
    finally:
        if 'conexion' in locals() and conexion:
            conexion.close()
"""
Script de utilidad para modificar el rol y departamento de un usuario
directamente en la base de datos SQLite.

Este script está diseñado para ser ejecutado de forma independiente
(fuera de la aplicación Flask) con el propósito de realizar cambios
administrativos directos en los roles de usuario.

Configuración:
    - USERNAME_A_MODIFICAR (str): El nombre de usuario cuyo rol se desea cambiar.
    - NUEVO_ROL (str): El nuevo rol que se asignará al usuario (ej. "jefe", "secretario", "usuario").
    - NUEVO_DEPARTAMENTO (str): El nuevo departamento que se asignará al usuario.

Proceso:
1. Construye la ruta a la base de datos `base_datos.db`.
2. Verifica si la base de datos existe.
3. Se conecta a la base de datos.
4. Ejecuta una consulta SQL UPDATE para cambiar el `rol` y `departamento`
   del usuario especificado por `USERNAME_A_MODIFICAR`.
5. Confirma si se realizó la actualización y muestra un mensaje de éxito o error.
"""