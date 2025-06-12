import sqlite3
import os

# --- Configuración ---
# Define el nombre de usuario y el nuevo rol aquí
USERNAME_A_MODIFICAR = "Lucas01"
NUEVO_ROL = "jefe"
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