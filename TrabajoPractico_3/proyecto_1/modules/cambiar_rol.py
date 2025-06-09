import sqlite3

# Conectar con la base de datos
conexion = sqlite3.connect("data/base_datos.db")
cursor = conexion.cursor()

# Cambiar el rol del usuario con ID 1
cursor.execute("UPDATE usuarios SET rol = ? WHERE id = ?", ("jefe", 1))

# Guardar cambios y cerrar conexión
conexion.commit()
conexion.close()

print("Rol actualizado correctamente")
