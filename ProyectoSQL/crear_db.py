import sqlite3

# Conectar a la base de datos (o crearla si no existe)
conn = sqlite3.connect('bddatos.db')
cursor = conn.cursor()

# Insertar un nuevo material
sql_insert = "INSERT INTO materiales (codigo, descripcion, unidad, precio, peso, tipo) VALUES (1, 'Tornillo', 'unidad', 0.50, 0.01, 'Metalico');"
cursor.execute(sql_insert)

conn.commit()

conn.close()