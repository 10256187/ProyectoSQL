import sqlite3

def revisar_columnas_materiales(nombre_db="datos.db"):
    try:
        conexion = sqlite3.connect(nombre_db)
        cursor = conexion.cursor()

        cursor.execute("PRAGMA table_info(materiales);")
        columnas = cursor.fetchall()

        if columnas:
            print("📋 Columnas encontradas en la tabla 'materiales':\n")
            for col in columnas:
                print(f"🔹 {col[1]} ({col[2]})")  # col[1] = nombre, col[2] = tipo
        else:
            print("⚠️ La tabla 'materiales' no existe.")
    except Exception as e:
        print(f"❌ Error revisando columnas: {e}")
    finally:
        conexion.close()

# Ejecutar función
revisar_columnas_materiales()