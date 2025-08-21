import sqlite3
from gestor_base import GestorBaseSQLite
from validaciones import leer_codigo, leer_descripcion, leer_unidad


class GestorEstructuraSQLite(GestorBaseSQLite):
    def __init__(self, nombre_db):
        campos = ["codigo", "descripcion", "unidad"]
        super().__init__(nombre_db, "estructura", campos)

    def crear_tabla(self):
        conexion = sqlite3.connect(self.nombre_db)
        cursor = conexion.cursor()

        # Tabla principal de estructura
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS estructura (
                codigo TEXT PRIMARY KEY,
                descripcion TEXT NOT NULL,
                unidad TEXT NOT NULL
            )
        """)

        # Tabla componentes
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS estructura_componentes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                estructura_codigo TEXT NOT NULL,
                tipo TEXT NOT NULL,
                componente_codigo TEXT NOT NULL,
                cantidad REAL NOT NULL,
                FOREIGN KEY (estructura_codigo) REFERENCES estructura(codigo)
            )
        """)

        conexion.commit()
        conexion.close()

    def agregar(self, codigo, descripcion, unidad, componentes=None):
        # 🔍 Validaciones
        codigo = leer_codigo(codigo)
        descripcion = leer_descripcion(descripcion)
        unidad = leer_unidad(unidad, tipo="estructura")

        # ✅ Agregar estructura principal
        super().agregar(codigo=codigo, descripcion=descripcion, unidad=unidad)

        # 🧩 Agregar componentes si los hay
        if componentes:
            conexion = sqlite3.connect(self.nombre_db)
            cursor = conexion.cursor()
            for comp in componentes:
                tipo = comp["tipo"]
                componente_codigo = leer_codigo(comp["componente_codigo"])
                cantidad = float(comp["cantidad"])  # ya validado externamente

                cursor.execute("""
                    INSERT INTO estructura_componentes (
                        estructura_codigo, tipo, componente_codigo, cantidad
                    ) VALUES (?, ?, ?, ?)
                """, (codigo, tipo, componente_codigo, cantidad))
            conexion.commit()
            conexion.close()
