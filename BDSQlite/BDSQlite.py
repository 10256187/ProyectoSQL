import sqlite3
import re

class Material:
    def __init__(self, codigo, descripcion, unidad, precio, peso):
        self.codigo = codigo
        self.descripcion = descripcion
        self.unidad = unidad
        self.precio = precio
        self.peso = peso

    def __str__(self):
        return f"{self.codigo} | {self.descripcion} | {self.unidad} | ${self.precio} | {self.peso}kg"

class GestorMaterialesSQLite:
    def __init__(self, archivo_db="materiales.db"):
        self.conn = sqlite3.connect(archivo_db)
        self.cursor = self.conn.cursor()
        self.crear_tabla()

    def crear_tabla(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS materiales (
                codigo TEXT PRIMARY KEY,
                descripcion TEXT NOT NULL,
                unidad TEXT NOT NULL,
                precio REAL NOT NULL,
                peso REAL NOT NULL
            )
        ''')
        self.conn.commit()

    
        print("\n📋 Lista de def agregar_material(self):
        print("\n🟢 Agregar nuevo material")

        while True:
            cod = input("Código (formato: AAAANNNN o AAAA-NNNN): ").strip().upper()

            if re.match(r"^[A-Z]{4}\d{4}$", cod):
                cod = cod[:4] + "-" + cod[4:]

            if not re.match(r"^[A-Z]{4}-\d{4}$", cod):
                print("❌ Código inválido. Usa 4 letras, guion, 4 números (ej: ABCD-1234).")
                continue

            self.cursor.execute("SELECT codigo FROM materiales WHERE codigo = ?", (cod,))
            if self.cursor.fetchone():
                print("⚠️ Ya existe un material con ese código.")
                continue

            codigo = cod
            break

        descripcion = input("Descripción: ").strip()
        
        unidades_validas = ["Ml","kM","Lb","Kg","Lt","cm","gL","Hz","Un","Sc","M³","M²","pg", "pt", "cñ"]
        while True:
            unidad = input("Unidad (ej: Ml, Un, m³): ").strip()
            if not re.match(r"^[A-Za-z][A-Za-z0-9]$", unidad):
                print("❌ Unidad inválida. Debe tener 2 caracteres: el primero una letra, el segundo letra o número.")
                continue
            break

        try:
            precio = float(input("Precio (ej: 2500): ").replace(",", "."))
            peso = float(input("Peso (por unidad de medida): ").replace(",", "."))
        except ValueError:
            print("❌ Error: el precio y el peso deben ser números.")
            return

        self.cursor.execute('''
            INSERT INTO materiales (codigo, descripcion, unidad, precio, peso)
            VALUES (?, ?, ?, ?, ?)
        ''', (codigo, descripcion, unidad, precio, peso))
        self.conn.commit()

        print("✅ Material agregado con éxito.")

    def ver_materiales(self):materiales registrados:")

        self.cursor.execute("SELECT * FROM materiales ORDER BY codigo")
        resultados = self.cursor.fetchall()

        if not resultados:
            print("⚠️ No hay materiales aún.")
            return

        for fila in resultados:
            codigo, descripcion, unidad, precio, peso = fila
            print(f"- {codigo} | {descripcion} | {unidad} | ${precio} | {peso}kg")

    def editar_material(self):
        print("\n✏️ Editar material")

        codigo = input("Ingrese el código del material a editar: ").strip().upper()
        if re.match(r"^[A-Z]{4}\d{4}$", codigo):
            codigo = codigo[:4] + "-" + codigo[4:]

        self.cursor.execute("SELECT * FROM materiales WHERE codigo = ?", (codigo,))
        resultado = self.cursor.fetchone()

        if not resultado:
            print("❌ No se encontró ningún material con ese código.")
            return

        actual = {
            "codigo": resultado[0],
            "descripcion": resultado[1],
            "unidad": resultado[2],
            "precio": resultado[3],
            "peso": resultado[4]
        }

        print(f"🔍 Editando {actual['codigo']} - {actual['descripcion']}")

        nueva_desc = input(f"Descripción nueva [{actual['descripcion']}]: ").strip()
        nueva_unidad = input(f"Unidad nueva [{actual['unidad']}]: ").strip()
        nuevo_precio = input(f"Precio nuevo [{actual['precio']}]: ").replace(",", ".").strip()
        nuevo_peso = input(f"Peso nuevo [{actual['peso']}]: ").replace(",", ".").strip()

        descripcion = nueva_desc if nueva_desc else actual["descripcion"]
        unidad = nueva_unidad if nueva_unidad else actual["unidad"]

        try:
            precio = float(nuevo_precio) if nuevo_precio else actual["precio"]
        except ValueError:
            print("❌ Precio inválido. Se mantiene el anterior.")
            precio = actual["precio"]

        try:
            peso = float(nuevo_peso) if nuevo_peso else actual["peso"]
        except ValueError:
            print("❌ Peso inválido. Se mantiene el anterior.")
            peso = actual["peso"]

        self.cursor.execute("""
            UPDATE materiales
            SET descripcion = ?, unidad = ?, precio = ?, peso = ?
            WHERE codigo = ?
        """, (descripcion, unidad, precio, peso, codigo))
        self.conn.commit()
        print("✅ Material actualizado con éxito.")

    def eliminar_material(self):
        print("\n🗑️ Eliminar material")

        codigo = input("Código del material a eliminar: ").strip().upper()
        if re.match(r"^[A-Z]{4}\d{4}$", codigo):
            codigo = codigo[:4] + "-" + codigo[4:]

        self.cursor.execute("SELECT * FROM materiales WHERE codigo = ?", (codigo,))
        material = self.cursor.fetchone()

        if not material:
            print("❌ No se encontró un material con ese código.")
            return

        print(f"🔍 Material encontrado: {material[0]} | {material[1]} | {material[2]} | ${material[3]} | {material[4]}kg")
        confirmar = input("¿Está seguro de que desea eliminarlo? (s/n): ").strip().lower()
        if confirmar != 's':
            print("❌ Operación cancelada.")
            return

        self.cursor.execute("DELETE FROM materiales WHERE codigo = ?", (codigo,))
        self.conn.commit()
        print("✅ Material eliminado con éxito.")

    def buscar_material(self):
        print("\n🔎 Buscar material por código")

        codigo = input("Código del material a buscar: ").strip().upper()
        if re.match(r"^[A-Z]{4}\d{4}$", codigo):
            codigo = codigo[:4] + "-" + codigo[4:]

        self.cursor.execute("SELECT * FROM materiales WHERE codigo = ?", (codigo,))
        resultado = self.cursor.fetchone()

        if resultado:
            codigo, descripcion, unidad, precio, peso = resultado
            print(f"✅ Encontrado: {codigo} | {descripcion} | {unidad} | ${precio} | {peso}kg")
        else:
            print("❌ No se encontró un material con ese código.")