import sqlite3
import os
from BDSQlite import GestorMaterialesSQLite

def probar_funciones_basicas():
    db_prueba = "test_materiales.db"
    
    # 🔄 Si ya existe, la eliminamos para hacer pruebas desde cero
    if os.path.exists(db_prueba):
        os.remove(db_prueba)
    
    # 🧠 Creamos el gestor de materiales apuntando a esta base de datos de prueba
    gestor = GestorMaterialesSQLite(archivo_db=db_prueba)

    # 🔸 Prueba: Agregar material
    print("🧪 Agregando material de prueba...")
    gestor.cursor.execute('''
        INSERT INTO materiales (codigo, descripcion, unidad, precio, peso)
        VALUES (?, ?, ?, ?, ?)
    ''', ("PRUE-0001", "Material de prueba", "Un", 1000.0, 2.5))
    gestor.conn.commit()

    gestor.cursor.execute("SELECT * FROM materiales WHERE codigo = ?", ("PRUE-0001",))
    material = gestor.cursor.fetchone()
    assert material is not None, "❌ No se agregó el material"

    # 🔸 Prueba: Editar material
    print("🧪 Editando material de prueba...")
    gestor.cursor.execute('''
        UPDATE materiales SET precio = ? WHERE codigo = ?
    ''', (1500.0, "PRUE-0001"))
    gestor.conn.commit()

    gestor.cursor.execute("SELECT precio FROM materiales WHERE codigo = ?", ("PRUE-0001",))
    nuevo_precio = gestor.cursor.fetchone()[0]
    assert nuevo_precio == 1500.0, "❌ El precio no se actualizó correctamente"

    # 🔸 Prueba: Eliminar material
    print("🧪 Eliminando material de prueba...")
    gestor.cursor.execute("DELETE FROM materiales WHERE codigo = ?", ("PRUE-0001",))
    gestor.conn.commit()

    gestor.cursor.execute("SELECT * FROM materiales WHERE codigo = ?", ("PRUE-0001",))
    eliminado = gestor.cursor.fetchone()
    assert eliminado is None, "❌ El material no se eliminó correctamente"

    print("✅ Todas las pruebas pasaron correctamente.")

if __name__ == "__main__":
    probar_funciones_basicas()