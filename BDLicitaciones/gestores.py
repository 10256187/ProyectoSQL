# gestores.py

import sqlite3
import re
from modelos import Material
from validaciones import leer_codigo, leer_descripcion, leer_unidad, leer_valor_unitario

# ------------------ GESTOR DE MATERIALES ------------------

class GestorMaterialesSQLite:
    def __init__(self, nombre_db="datos.db"):
        self.nombre_db = nombre_db
        self._crear_tabla()

    def _crear_tabla(self):
        with sqlite3.connect(self.nombre_db) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS materiales (
                    codigo TEXT PRIMARY KEY,
                    descripcion TEXT NOT NULL,
                    unidad TEXT NOT NULL,
                    precio REAL NOT NULL,
                    peso REAL NOT NULL
                )
            """)
            conn.commit()

    def _existe_codigo(self, codigo):
        with sqlite3.connect(self.nombre_db) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT codigo FROM materiales WHERE codigo = ?", (codigo,))
            return cursor.fetchone() is not None

    def buscar_material(self, codigo):
        with sqlite3.connect(self.nombre_db) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM materiales WHERE codigo = ?", (codigo,))
            return cursor.fetchone()


    def agregar_material(self):
        print("\n🟢 Agregar nuevo material")
        codigo = leer_codigo("Código (AAAA-NNNN): ", self._existe_codigo)
        descripcion = leer_descripcion("Descripción: ")

        unidades_validas = ["ML", "M³", "M²", "KM", "LB", "KG", "LT", "CM", "GL", "GB", "HZ", "UN", "SC", "CT", "PT", "CÑ"]
        unidad = leer_unidad(unidades_validas, prompt="Unidad (ej. KG, LT, M²): ")

        precio = leer_valor_unitario("Precio: ")
        peso = leer_valor_unitario("Peso: ")
        
        nuevo = Material(codigo, descripcion, unidad, precio, peso)

        with sqlite3.connect(self.nombre_db) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO materiales (codigo, descripcion, unidad, precio, peso)
                VALUES (?, ?, ?, ?, ?)
            """, (nuevo.codigo, nuevo.descripcion, nuevo.unidad, nuevo.precio, nuevo.peso))
            conn.commit()

        print("✅ Material agregado con éxito.")

    def ver_materiales(self):
        print("\n📦 Lista de materiales:")
        with sqlite3.connect(self.nombre_db) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT codigo, descripcion, unidad, precio, peso FROM materiales")
            materiales = cursor.fetchall()

            if not materiales:
                print("⚠️ No hay materiales registrados.")
                return

            for codigo, descripcion, unidad, precio, peso in materiales:
                try:
                    precio = float(precio)
                except ValueError:
                    precio = 0.0
                print(f"- {codigo} | {descripcion} | {unidad} | ${precio:,.2f} | {peso}")

    def editar_material(self, codigo_original):
        print("\n✏️ Editar material")
        codigo = leer_codigo("Código: ")

        with sqlite3.connect(self.nombre_db) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM materiales WHERE codigo = ?", (codigo,))
            resultado = cursor.fetchone()

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

            print(f"🔍 Editando: {actual['codigo']} (el código no se puede cambiar)")
            descripcion = leer_descripcion("Descripción: ", permitir_vacio=True) or actual["descripcion"]

            unidades_validas = ["ML", "M³", "M²", "KM", "LB", "KG", "LT", "CM", "GL", "GB", "HZ", "UN", "SC", "CT", "PT", "CÑ"]
            unidad = leer_unidad(unidades_validas, prompt="Unidad (ej. KG, LT, M²): ") or actual["unidad"]

            precio = leer_valor_unitario("Precio: ", permitir_vacio=True)
            if precio is None:
                precio = actual["precio"]

            try:
                peso_input = input("Peso: ").replace(",", ".").strip()
                peso = float(peso_input) if peso_input else actual["peso"]
            except ValueError:
                print("❌ Peso inválido. Se mantiene el anterior.")
                peso = actual["peso"]

            cursor.execute("""
                UPDATE materiales
                SET descripcion = ?, unidad = ?, precio = ?, peso = ?
                WHERE codigo = ?
            """, (descripcion, unidad, precio, peso, codigo))
            conn.commit()

            print("✅ Material actualizado con éxito.")

# ------------------ GESTOR DE MANO DE OBRA ------------------

class GestorManoObraSQLite:
    def __init__(self, nombre_db="datos.db"):
        self.nombre_db = nombre_db
        self._crear_tabla()

    def _crear_tabla(self):
        with sqlite3.connect(self.nombre_db) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS mano_obra (
                    codigo TEXT PRIMARY KEY,
                    descripcion TEXT NOT NULL,
                    unidad TEXT NOT NULL,
                    precio REAL NOT NULL
                )
            """)
            conn.commit()

    def _existe_codigo(self, codigo):
        with sqlite3.connect(self.nombre_db) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT codigo FROM mano_obra WHERE codigo = ?", (codigo,))
            return cursor.fetchone() is not None

    def agregar_mano_obra(self):
        print("\n🟢 Agregar mano de obra")
        codigo = leer_codigo("Código mobra: ", self._existe_codigo)
        descripcion = leer_descripcion("Descripción: ")

        unidades_validas = ["HH", "DD", "JN", "MS", "HN"]
        unidad = leer_unidad(unidades_validas, prompt="Unidad (HH, DD, JN, MS, HN): ")

        precio = leer_valor_unitario("Precio: ")

        with sqlite3.connect(self.nombre_db) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO mano_obra (codigo, descripcion, unidad, precio)
                VALUES (?, ?, ?, ?)
            """, (codigo, descripcion, unidad, precio))
            conn.commit()

        print("✅ Trabajador agregado con éxito.")

    def ver_mano_obra(self):
        print("\n📦 Lista de mano de obra")
        with sqlite3.connect(self.nombre_db) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT codigo, descripcion, unidad, precio FROM mano_obra")
            mano_obra = cursor.fetchall()

            if not mano_obra:
                print("⚠️ No hay mano de obra registrados.")
                return

            for codigo, descripcion, unidad, precio in mano_obra:
                try:
                    precio = float(precio)
                except ValueError:
                    precio = 0.0
                print(f"- {codigo} | {descripcion} | {unidad} | ${precio:,.2f}")

    def editar_mano_obra(self):
        print("\n✏️ Editar mano de obra")
        codigo = leer_codigo("Código: ")

        with sqlite3.connect(self.nombre_db) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM mano_obra WHERE codigo = ?", (codigo,))
            resultado = cursor.fetchone()

            if not resultado:
                print("❌ No se encontró mano de obra con ese código.")
                return

            actual = {
                "codigo": resultado[0],
                "descripcion": resultado[1],
                "unidad": resultado[2],
                "precio": resultado[3]
            }

            print(f"🔍 Editando: {actual['codigo']} (el código no se puede cambiar)")

            descripcion = leer_descripcion("Descripción: ", permitir_vacio=True) or actual["descripcion"]

            unidades_validas = ["HH", "DD", "JN", "MS", "HN"]
            unidad = leer_unidad(unidades_validas, prompt="Unidad (HH, DD, JN, MS, HN): ") or actual["unidad"]

            precio = leer_valor_unitario("Precio: ", permitir_vacio=True)
            if precio is None:
                precio = actual["precio"]

            cursor.execute("""
                UPDATE mano_obra
                SET descripcion = ?, unidad = ?, precio = ?
                WHERE codigo = ?
            """, (descripcion, unidad, precio, codigo))
            conn.commit()

            print("✅ Mano de obra actualizada con éxito.")

class GestorHerramientasSQLite:
    def __init__(self, nombre_db="datos.db"):
        self.nombre_db = nombre_db
        self._crear_tabla()

    def _crear_tabla(self):
        with sqlite3.connect(self.nombre_db) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS herramientas (
                    codigo TEXT PRIMARY KEY,
                    descripcion TEXT NOT NULL,
                    unidad TEXT NOT NULL,
                    precio REAL NOT NULL
                )
            """)
            conn.commit()

    def _existe_codigo(self, codigo):
        with sqlite3.connect(self.nombre_db) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT codigo FROM herramientas WHERE codigo = ?", (codigo,))
            return cursor.fetchone() is not None

    def agregar_herramienta(self):
        print("\n🛠️ Agregar herramienta")

        codigo = leer_codigo("Código herramienta: ", self._existe_codigo)
        descripcion = leer_descripcion("Descripción: ")

        unidades_validas = ["DD", "MS", "HR"]
        unidad = leer_unidad(unidades_validas, prompt="Unidad (DD, MS, HR): ")

        precio = leer_valor_unitario("Precio: ")

        with sqlite3.connect(self.nombre_db) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO herramientas (codigo, descripcion, unidad, precio)
                VALUES (?, ?, ?, ?)
            """, (codigo, descripcion, unidad, precio))
            conn.commit()

        print("✅ Herramienta agregada con éxito.")

    def ver_herramientas(self):
        print("\n🧰 Lista de herramientas")
        with sqlite3.connect(self.nombre_db) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT codigo, descripcion, unidad, precio FROM herramientas")
            herramientas = cursor.fetchall()

            if not herramientas:
                print("⚠️ No hay herramientas registradas.")
                return

            for codigo, descripcion, unidad, precio in herramientas:
                try:
                    precio = float(precio)
                except ValueError:
                    precio = 0.0

                print(f"- {codigo} | {descripcion} | {unidad} | ${precio:,.2f}")

    def editar_herramienta(self):
        print("\n✏️ Editar herramienta")

        codigo = leer_codigo("Código: ")

        with sqlite3.connect(self.nombre_db) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM herramientas WHERE codigo = ?", (codigo,))
            resultado = cursor.fetchone()

            if not resultado:
                print("❌ No se encontró herramienta con ese código.")
                return

            actual = {
                "codigo": resultado[0],
                "descripcion": resultado[1],
                "unidad": resultado[2],
                "precio": resultado[3],
            }

            print(f"🔍 Editando: {actual['codigo']}")

            descripcion = leer_descripcion("Descripción: ", permitir_vacio=True) or actual["descripcion"]

            unidades_validas = ["DD", "MS", "HR"]
            unidad = leer_unidad(unidades_validas, prompt="Unidad (DD, MS, HR): ") or actual["unidad"]

            precio = leer_valor_unitario("Precio: ", permitir_vacio=True)
            if precio is None:
                precio = actual["precio"]

            cursor.execute("""
                UPDATE herramientas
                SET descripcion = ?, unidad = ?, precio = ?
                WHERE codigo = ?
            """, (descripcion, unidad, precio, codigo))
            conn.commit()

            print("✅ Herramienta actualizada con éxito.")


class GestorTransporteSQLite:
    def __init__(self, nombre_db="datos.db"):
        self.nombre_db = nombre_db
        self._crear_tabla()

    def _crear_tabla(self):
        with sqlite3.connect(self.nombre_db) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS transporte (
                    codigo TEXT PRIMARY KEY,
                    descripcion TEXT NOT NULL,
                    unidad TEXT NOT NULL,
                    precio REAL NOT NULL
                )
            """)
            conn.commit()

    def _existe_codigo(self, codigo):
        with sqlite3.connect(self.nombre_db) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT codigo FROM transporte WHERE codigo = ?", (codigo,))
            return cursor.fetchone() is not None

    def agregar_transporte(self):
        print("\n🚚 Agregar transporte")

        codigo = leer_codigo("Código transporte: ", self._existe_codigo)
        descripcion = leer_descripcion("Descripción: ")

        unidades_validas = ["TK", "VJ", "M³", "MS", "DD", "HR","VK"]
        unidad = leer_unidad(unidades_validas, prompt="Unidad (TK, VJ, M³, MS, DD, HR): ")

        precio = leer_valor_unitario("Precio:")

        with sqlite3.connect(self.nombre_db) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO transporte (codigo, descripcion, unidad, precio)
                VALUES (?, ?, ?, ?)
            """, (codigo, descripcion, unidad, precio))
            conn.commit()

        print("✅ Transporte agregado con éxito.")

    def ver_transporte(self):
        print("\n🚚 Lista de transporte:")
        with sqlite3.connect(self.nombre_db) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT codigo, descripcion, unidad, precio FROM transporte")
            transportes = cursor.fetchall()

            if not transportes:
                print("⚠️ No hay transportes registrados.")
                return

            for codigo, descripcion, unidad, precio in transportes:
                try:
                    precio = float(precio)
                except ValueError:
                    precio = 0.0
                print(f"- {codigo} | {descripcion} | {unidad} | ${precio:,.2f}")

    def editar_transporte(self):
        print("\n✏️ Editar transporte")

        codigo = leer_codigo("Código: ")

        with sqlite3.connect(self.nombre_db) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM transporte WHERE codigo = ?", (codigo,))
            resultado = cursor.fetchone()

            if not resultado:
                print("❌ No se encontró transporte con ese código.")
                return

            actual = {
                "codigo": resultado[0],
                "descripcion": resultado[1],
                "unidad": resultado[2],
                "precio": resultado[3],
            }

            print(f"🔍 Editando: {actual['codigo']} (el código no se puede cambiar)")

            descripcion = leer_descripcion("Descripción: ", permitir_vacio=True) or actual["descripcion"]
            unidades_validas = ["TK", "VJ", "M³", "MS", "DD", "HR","VK"]
            unidad = leer_unidad(unidades_validas, prompt="Unidad (TK, VJ, M³, MS, DD, HR): ") or actual["unidad"]
            precio = leer_valor_unitario("Precio: ", permitir_vacio=True)
            if precio is None:
                precio = actual["precio"]

            cursor.execute("""
                UPDATE transporte
                SET descripcion = ?, unidad = ?, precio = ?
                WHERE codigo = ?
            """, (descripcion, unidad, precio, codigo))
            conn.commit()

        print("✅ Transporte actualizado con éxito.")
