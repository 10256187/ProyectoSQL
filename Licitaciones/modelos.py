# modelos.py
import sqlite3
from validaciones import leer_codigo, leer_descripcion, leer_unidad, leer_valor_numerico


class Material:
    def __init__(self, codigo, descripcion, unidad, precio, peso):
        self.codigo = codigo
        self.descripcion = descripcion
        self.unidad = unidad
        self.precio = precio
        self.peso = peso

    def __str__(self):
        return f"{self.codigo} | {self.descripcion} | {self.unidad} | ${self.precio:,.2f} | {self.peso:,.2f}"


class ManoDeObra:
    def __init__(self, codigo, descripcion, unidad, precio):
        self.codigo = codigo
        self.descripcion = descripcion
        self.unidad = unidad
        self.precio = precio
    def __str__(self):
        return f"{self.codigo} | {self.descripcion} | {self.unidad} | ${self.precio:,.2f}"

class Herramienta:
    def __init__(self, codigo, descripcion, unidad, precio):
        self.codigo = codigo
        self.descripcion = descripcion
        self.unidad = unidad
        self.precio = precio

    def __str__(self):
        return f"{self.codigo} | {self.descripcion} | {self.unidad} | ${self.precio:,.2f}"


class Transporte:
    def __init__(self, codigo, descripcion, unidad, precio):
        self.codigo = codigo
        self.descripcion = descripcion
        self.unidad = unidad
        self.precio = precio

    def __str__(self):
        return f"{self.codigo} | {self.descripcion} | {self.unidad} | ${self.precio:,.2f}"


class Estructura:
    def __init__(self, nombre_base="datos.db"):
        self.nombre_base = nombre_base
        self.crear_tablas()

    def conectar(self):
        return sqlite3.connect(self.nombre_base)

    def crear_tablas(self):
        conexion = self.conectar()
        cursor = conexion.cursor()

        # Tabla principal de estructuras
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS estructuras (
            codigo TEXT PRIMARY KEY,
            descripcion TEXT NOT NULL,
            unidad TEXT NOT NULL
        )
        """)

        # Tablas de relación para insumos
        for tipo in ["materiales", "mano_obra", "herramientas", "transporte"]:
            cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS estructura_{tipo} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                codigo_estructura TEXT NOT NULL,
                codigo_insumo TEXT NOT NULL,
                cantidad REAL NOT NULL,
                costo_unitario REAL NOT NULL,
                costo_parcial REAL NOT NULL,
                FOREIGN KEY (codigo_estructura) REFERENCES estructuras(codigo)
            )
            """)
        conexion.commit()
        conexion.close()

    def agregar_estructura(self):
        print("📦 Agregar nueva estructura")
        codigo = leer_codigo()
        descripcion = leer_descripcion()
        unidad = leer_unidad("estructura")

        conexion = self.conectar()
        cursor = conexion.cursor()
        cursor.execute(
            "INSERT INTO estructuras (codigo, descripcion, unidad) VALUES (?, ?, ?)",
            (codigo, descripcion, unidad)
        )
        conexion.commit()
        conexion.close()
        print(f"✅ Estructura '{descripcion}' agregada correctamente.")

    def agregar_insumo_a_estructura(self, tipo):
        print(f"➕ Agregar {tipo.replace('_', ' ')} a estructura")
        codigo_estructura = leer_codigo("Código de la estructura")
        codigo_insumo = leer_codigo("Código del insumo")
        cantidad = leer_valor_numerico("Cantidad")  # reutilizamos validación de número
        costo_unitario = leer_valor_numerico("Costo unitario")
        costo_parcial = cantidad * costo_unitario

        conexion = self.conectar()
        cursor = conexion.cursor()
        cursor.execute(f"""
            INSERT INTO estructura_{tipo} 
            (codigo_estructura, codigo_insumo, cantidad, costo_unitario, costo_parcial)
            VALUES (?, ?, ?, ?, ?)
        """, (codigo_estructura, codigo_insumo, cantidad, costo_unitario, costo_parcial))
        conexion.commit()
        conexion.close()
        print(f"✅ {tipo.replace('_', ' ').capitalize()} agregado a estructura.")

    def ver_detalle_estructura(self, codigo_estructura):
        conexion = self.conectar()
        cursor = conexion.cursor()

        # Datos de la estructura
        cursor.execute("SELECT codigo, descripcion, unidad FROM estructuras WHERE codigo = ?", (codigo_estructura,))
        estructura = cursor.fetchone()
        if not estructura:
            print("❌ Estructura no encontrada.")
            return

        print(f"\n📦 Estructura: {estructura[1]} ({estructura[0]}) - Unidad: {estructura[2]}")
        total_general = 0

        # Listar insumos por tipo
        for tipo in ["materiales", "mano_obra", "herramientas", "transporte"]:
            cursor.execute(f"""
                SELECT codigo_insumo, cantidad, costo_unitario, costo_parcial
                FROM estructura_{tipo}
                WHERE codigo_estructura = ?
            """, (codigo_estructura,))
            registros = cursor.fetchall()
            if registros:
                print(f"\n📋 {tipo.replace('_', ' ').capitalize()}:")
                for r in registros:
                    print(f"   - {r[0]} | Cant: {r[1]} | Unit: {r[2]} | Parcial: {r[3]}")
                    total_general += r[3]

        print(f"\n💰 Total Estructura: {total_general}")
        conexion.close()