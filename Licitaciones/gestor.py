import sqlite3
from rich.table import Table
from rich.console import Console
from validaciones import leer_codigo, leer_descripcion, leer_unidad, leer_valor_numerico

console = Console()

# ------------------------------
# Clase base para todos los gestores
# ------------------------------
class GestorBaseSQLite:
    def __init__(self, nombre_base, tabla, campos):
        self.nombre_base = nombre_base
        self.tabla = tabla
        self.campos = campos
        self.crear_tabla()

    def crear_tabla(self):
        conexion = sqlite3.connect(self.nombre_base)
        cursor = conexion.cursor()
        campos_sql = ", ".join([f"{nombre} {tipo}" for nombre, tipo in self.campos.items()])
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {self.tabla} ({campos_sql})")
        conexion.commit()
        conexion.close()

    def agregar_registro(self, datos):
        conexion = sqlite3.connect(self.nombre_base)
        cursor = conexion.cursor()
        placeholders = ", ".join(["?"] * len(datos))
        cursor.execute(
            f"INSERT INTO {self.tabla} ({', '.join(self.campos.keys())}) VALUES ({placeholders})",
            datos
        )
        conexion.commit()
        conexion.close()
        console.print(f"✅ Registro agregado en {self.tabla} con éxito.", style="bold green")

    def ver_registros(self):
        conexion = sqlite3.connect(self.nombre_base)
        cursor = conexion.cursor()
        cursor.execute(f"SELECT * FROM {self.tabla}")
        registros = cursor.fetchall()
        conexion.close()

        if not registros:
            console.print(f"⚠ No hay registros en {self.tabla}.", style="bold yellow")
            return

        table = Table(title=f"Tabla {self.tabla}")
        for campo in self.campos.keys():
            table.add_column(campo, style="cyan")
        for registro in registros:
            table.add_row(*[str(campo) for campo in registro])
        console.print(table)

    def editar_registro(self, codigo):
        conexion = sqlite3.connect(self.nombre_base)
        cursor = conexion.cursor()
        cursor.execute(f"SELECT * FROM {self.tabla} WHERE codigo=?", (codigo,))
        registro = cursor.fetchone()

        if not registro:
            console.print(f"❌ No se encontró el código {codigo} en {self.tabla}.", style="bold red")
            conexion.close()
            return

        nuevos_datos = []
        for i, campo in enumerate(self.campos.keys()):
            if campo == "codigo":
                nuevos_datos.append(codigo)
                continue
            nuevo_valor = input(f"{campo} actual ({registro[i]}): ") or registro[i]
            nuevos_datos.append(nuevo_valor)

        cursor.execute(
            f"UPDATE {self.tabla} SET {', '.join([f'{campo}=?' for campo in self.campos.keys() if campo != 'codigo'])} WHERE codigo=?",
            (*nuevos_datos[1:], codigo)
        )
        conexion.commit()
        conexion.close()
        console.print(f"✏ Registro {codigo} editado en {self.tabla}.", style="bold green")

    def exportar_csv(self, archivo_csv):
        conexion = sqlite3.connect(self.nombre_base)
        cursor = conexion.cursor()
        cursor.execute(f"SELECT * FROM {self.tabla}")
        registros = cursor.fetchall()
        conexion.close()

        if not registros:
            console.print(f"⚠ No hay datos para exportar en {self.tabla}.", style="bold yellow")
            return

        import csv
        with open(archivo_csv, mode="w", newline="", encoding="utf-8") as archivo:
            writer = csv.writer(archivo)
            writer.writerow(self.campos.keys())
            writer.writerows(registros)

        console.print(f"📄 Datos exportados a {archivo_csv} correctamente.", style="bold green")


class GestorEstructuraSQLite:
    class GestorEstructurasSQLite:
        def __init__(self, nombre_base="datos.db"):
            self.nombre_base = nombre_base
            self.crear_tablas()

        def crear_tablas(self):
            conexion = sqlite3.connect(self.nombre_base)
            cursor = conexion.cursor()
            
                # Tabla principal de estructuras
            cursor.execute("""
                    CREATE TABLE IF NOT EXISTS estructuras (
                        codigo TEXT PRIMARY KEY,
                        descripcion TEXT NOT NULL,
                        unidad TEXT NOT NULL
                    )
                """)

                # Tablas intermedias para componentes
            tablas_componentes = {
                    "estructura_materiales": "materiales",
                    "estructura_mano_obra": "mano_obra",
                    "estructura_herramientas": "herramientas",
                    "estructura_transporte": "transporte"
                }
            for tabla, ref_tabla in tablas_componentes.items():
                    cursor.execute(f"""
                        CREATE TABLE IF NOT EXISTS {tabla} (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            estructura_codigo TEXT NOT NULL,
                            componente_codigo TEXT NOT NULL,
                            cantidad REAL NOT NULL,
                            FOREIGN KEY (estructura_codigo) REFERENCES estructuras(codigo),
                            FOREIGN KEY (componente_codigo) REFERENCES {ref_tabla}(codigo)
                        )
                    """)

            conexion.commit()
            conexion.close()

        def agregar_estructura(self):
            console.print("[bold cyan]➕ Agregar nueva estructura[/bold cyan]")
            codigo = leer_codigo("Código de la estructura (único)")
            descripcion = leer_descripcion()
            unidad = leer_unidad("estructura")

            conexion = sqlite3.connect(self.nombre_base)
            cursor = conexion.cursor()
            try:
                cursor.execute("INSERT INTO estructuras VALUES (?, ?, ?)", (codigo, descripcion, unidad))
                conexion.commit()
                console.print("[green]✅ Estructura agregada correctamente[/green]")
            except sqlite3.IntegrityError:
                console.print("[red]❌ Error: ya existe una estructura con ese código[/red]")
            conexion.close()

        def asociar_componente(self, tipo):
            """
                tipo: 'materiales', 'mano_obra', 'herramientas', 'transporte'
            """
            console.print(f"[bold cyan]🔗 Asociar {tipo} a una estructura[/bold cyan]")
            estructura_codigo = leer_codigo("Código de la estructura")
            componente_codigo = leer_codigo(f"Código del {tipo}")
            cantidad = leer_valor_numerico()

            conexion = sqlite3.connect(self.nombre_base)
            cursor = conexion.cursor()
            tabla_relacion = f"estructura_{tipo}"
            cursor.execute(f"""
                INSERT INTO {tabla_relacion} (estructura_codigo, componente_codigo, cantidad)
                VALUES (?, ?, ?)
            """, (estructura_codigo, componente_codigo, cantidad))
            conexion.commit()
            conexion.close()
            console.print(f"[green]✅ {tipo.capitalize()} asociado correctamente[/green]")
        
        def ver_estructura(self, codigo):
            conexion = sqlite3.connect(self.nombre_base)
            cursor = conexion.cursor()

            cursor.execute("SELECT descripcion, unidad FROM estructuras WHERE codigo=?", (codigo,))
            estructura = cursor.fetchone()
            if not estructura:
                console.print("[red]❌ Estructura no encontrada[/red]")
                conexion.close()
                return

            descripcion, unidad = estructura
            console.print(f"[bold]Estructura:[/bold] {codigo} - {descripcion} ({unidad})")

            tablas_componentes = {
                "materiales": "estructura_materiales",
                "mano_obra": "estructura_mano_obra",
                "herramientas": "estructura_herramientas",
                "transporte": "estructura_transporte"
            }

            costo_total = 0
            for tipo, tabla_relacion in tablas_componentes.items():
                cursor.execute(f"""
                    SELECT ec.componente_codigo, ec.cantidad, t.precio
                    FROM {tabla_relacion} ec
                    JOIN {tipo} t ON ec.componente_codigo = t.codigo
                    WHERE ec.estructura_codigo = ?
                """, (codigo,))
                resultados = cursor.fetchall()

                if resultados:
                    table = Table(title=f"{tipo.capitalize()}")
                    table.add_column("Código")
                    table.add_column("Cantidad")
                    table.add_column("Precio")
                    table.add_column("Valor Parcial")

                    for comp_codigo, cantidad, precio in resultados:
                        valor_parcial = cantidad * precio
                        costo_total += valor_parcial
                        table.add_row(comp_codigo, str(cantidad), f"{precio:,.2f}", f"{valor_parcial:,.2f}")

                    console.print(table)

            console.print(f"[bold green]💰 Costo Total: {costo_total:,.2f}[/bold green]")
            conexion.close()

# ------------------------------
# Gestores específicos
# ------------------------------
class GestorMaterialesSQLite(GestorBaseSQLite):
    def __init__(self, nombre_base):
        campos = {
            "codigo": "TEXT PRIMARY KEY",
            "descripcion": "TEXT",
            "unidad": "TEXT",
            "precio": "REAL"
        }
        super().__init__(nombre_base, "materiales", campos)

    def agregar_material(self):
        codigo = leer_codigo()
        descripcion = leer_descripcion()
        unidad = leer_unidad("material")
        precio = leer_valor_numerico()
        self.agregar_registro((codigo, descripcion, unidad, precio))


class GestorManoObraSQLite(GestorBaseSQLite):
    def __init__(self, nombre_base):
        campos = {
            "codigo": "TEXT PRIMARY KEY",
            "descripcion": "TEXT",
            "unidad": "TEXT",
            "precio": "REAL"
        }
        super().__init__(nombre_base, "mano_obra", campos)

    def agregar_mano_obra(self):
        codigo = leer_codigo()
        descripcion = leer_descripcion()
        unidad = leer_unidad("mano_obra")
        precio = leer_valor_numerico()
        self.agregar_registro((codigo, descripcion, unidad, precio))


class GestorHerramientasSQLite(GestorBaseSQLite):
    def __init__(self, nombre_base):
        campos = {
            "codigo": "TEXT PRIMARY KEY",
            "descripcion": "TEXT",
            "unidad": "TEXT",
            "precio": "REAL"
        }
        super().__init__(nombre_base, "herramientas", campos)

    def agregar_herramienta(self):
        codigo = leer_codigo()
        descripcion = leer_descripcion()
        unidad = leer_unidad("herramienta")
        precio = leer_valor_numerico()
        self.agregar_registro((codigo, descripcion, unidad, precio))


class GestorTransporteSQLite(GestorBaseSQLite):
    def __init__(self, nombre_base):
        campos = {
            "codigo": "TEXT PRIMARY KEY",
            "descripcion": "TEXT",
            "unidad": "TEXT",
            "precio": "REAL"
        }
        super().__init__(nombre_base, "transporte", campos)

    def agregar_transporte(self):
        codigo = leer_codigo()
        descripcion = leer_descripcion()
        unidad = leer_unidad("transporte")
        precio = leer_valor_numerico()
        self.agregar_registro((codigo, descripcion, unidad, precio))
        

class GestorEstructuraSQLite(GestorBaseSQLite):
    def __init__(self, nombre_base):
        super().__init__(nombre_base)
        self.crear_tablas()

    def crear_tablas(self):
        conexion = sqlite3.connect(self.nombre_base)
        cursor = conexion.cursor()

        # Tabla principal de estructuras
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS estructuras (
                codigo TEXT PRIMARY KEY,
                descripcion TEXT NOT NULL,
                unidad TEXT NOT NULL
            )
        """)

        # Tablas de insumos por estructura
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS estructura_materiales (
                codigo_estructura TEXT,
                codigo TEXT,
                descripcion TEXT,
                unidad TEXT,
                cantidad REAL,
                costo_unitario REAL,
                total REAL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS estructura_mano_obra (
                codigo_estructura TEXT,
                codigo TEXT,
                descripcion TEXT,
                unidad TEXT,
                cantidad REAL,
                costo_unitario REAL,
                total REAL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS estructura_herramientas (
                codigo_estructura TEXT,
                codigo TEXT,
                descripcion TEXT,
                unidad TEXT,
                cantidad REAL,
                costo_unitario REAL,
                total REAL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS estructura_transporte (
                codigo_estructura TEXT,
                codigo TEXT,
                descripcion TEXT,
                unidad TEXT,
                cantidad REAL,
                costo_unitario REAL,
                total REAL
            )
        """)

        conexion.commit()
        conexion.close()

    def agregar_estructura(self):
        from validaciones import leer_codigo, leer_descripcion, leer_unidad

        codigo = leer_codigo()
        descripcion = leer_descripcion()
        unidad = leer_unidad("estructura")

        conexion = sqlite3.connect(self.nombre_base)
        cursor = conexion.cursor()
        try:
            cursor.execute(
                "INSERT INTO estructuras (codigo, descripcion, unidad) VALUES (?, ?, ?)",
                (codigo, descripcion, unidad)
            )
            conexion.commit()
            print(f"✅ Estructura '{descripcion}' agregada con éxito.")
        except sqlite3.IntegrityError:
            print("⚠️ Ya existe una estructura con ese código.")
        finally:
            conexion.close()

    def agregar_insumo_a_estructura(self, tipo):
        """
        tipo: 'material', 'mano_obra', 'herramienta', 'transporte'
        """
        from validaciones import leer_codigo

        conexion = sqlite3.connect(self.nombre_base)
        cursor = conexion.cursor()

        codigo_estructura = input("Ingrese el código de la estructura: ").strip()
        cursor.execute("SELECT * FROM estructuras WHERE codigo=?", (codigo_estructura,))
        estructura = cursor.fetchone()
        if not estructura:
            print("⚠️ No existe esa estructura.")
            conexion.close()
            return

        codigo_insumo = leer_codigo()
        tabla_insumo = {
            "material": "materiales",
            "mano_obra": "mano_obra",
            "herramienta": "herramientas",
            "transporte": "transporte"
        }[tipo]

        cursor.execute(f"SELECT descripcion, unidad, precio FROM {tabla_insumo} WHERE codigo=?", (codigo_insumo,))
        insumo = cursor.fetchone()
        if not insumo:
            print(f"⚠️ No existe ese {tipo}.")
            conexion.close()
            return

        descripcion, unidad, precio = insumo
        cantidad = float(input("Ingrese la cantidad: "))
        total = cantidad * precio

        tabla_estructura = f"estructura_{tabla_insumo}"
        cursor.execute(f"""
            INSERT INTO {tabla_estructura} 
            (codigo_estructura, codigo, descripcion, unidad, cantidad, costo_unitario, total) 
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (codigo_estructura, codigo_insumo, descripcion, unidad, cantidad, precio, total))

        conexion.commit()
        conexion.close()
        print(f"✅ {tipo.capitalize()} agregado a la estructura.")

    def ver_estructura(self):
        codigo_estructura = input("Ingrese el código de la estructura: ").strip()

        conexion = sqlite3.connect(self.nombre_base)
        cursor = conexion.cursor()

        cursor.execute("SELECT * FROM estructuras WHERE codigo=?", (codigo_estructura,))
        estructura = cursor.fetchone()
        if not estructura:
            print("⚠️ No existe esa estructura.")
            conexion.close()
            return

        print(f"\n📋 Estructura: {estructura[1]} ({estructura[0]}) - Unidad: {estructura[2]}")

        total_general = 0
        for tipo in ["materiales", "mano_obra", "herramientas", "transporte"]:
            tabla = f"estructura_{tipo}"
            cursor.execute(f"SELECT descripcion, cantidad, costo_unitario, total FROM {tabla} WHERE codigo_estructura=?", (codigo_estructura,))
            registros = cursor.fetchall()
            if registros:
                print(f"\n🔹 {tipo.capitalize()}:")
                for r in registros:
                    print(f"   {r[0]} - Cant: {r[1]} - Costo Unit: {r[2]} - Total: {r[3]}")
                    total_general += r[3]

        print(f"\n💰 Costo total de la estructura: {total_general}")
        conexion.close()
