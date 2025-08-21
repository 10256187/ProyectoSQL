# ------------------ GESTOR MATERIALES ------------------

class GestorMaterialesSQLite(GestorBaseSQLite):
      def __init__(self, nombre_db):
        campos = ["codigo", "descripcion", "unidad", "precio", "peso"]
        super().__init__(nombre_db, "materiales", campos)

        def crear_tabla(self):
            with sqlite3.connect(self.nombre_db) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS materiales (
                        codigo TEXT PRIMARY KEY,
                        descripcion TEXT NOT NULL,
                        unidad TEXT NOT NULL,
                        precio REAL NOT NULL,
                        peso REAL NOT NULL
                    )
                ''')
                conn.commit()

        def _existe_codigo(self, codigo):
            with sqlite3.connect(self.nombre_db) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT codigo FROM datos WHERE codigo = ?", (codigo,))
                return cursor.fetchone() is not None

            def buscar_material(self, codigo):
                with sqlite3.connect(self.nombre_db) as conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT * FROM datos WHERE codigo = ?", (codigo,))
                    return cursor.fetchone()

            def exportar_csv(self, archivo_csv):
                try:
                    conexion = sqlite3.connect(self.nombre_db)
                    cursor = conexion.cursor()
                    cursor.execute(f"SELECT * FROM {self.nombre_tabla}")
                    datos = cursor.fetchall()
                    columnas = [descripcion[0] for descripcion in cursor.description]

                    with open(archivo_csv, mode='w', newline='', encoding='utf-8') as archivo:
                        writer = csv.writer(archivo)
                        writer.writerow(columnas)
                        writer.writerows(datos)

                    print(f"✅ Datos exportados exitosamente a '{archivo_csv}'.")
                except Exception as e:
                    print(f"❌ Error al exportar: {e}")
                finally:
                    conexion.close()

        def agregar_insumo(self):
            print(f"\n➕ Agregar {self.nombre_tabla.capitalize()}")
            codigo = leer_codigo("Código: ", self._existe_codigo)
            descripcion = leer_descripcion("Descripción: ")

            unidades_validas = ["ML", "M³", "M²", "KM", "LB", "KG", "LT", "CM", "GL", "GB", "HZ", "UN", "SC", "CT", "PT", "CÑ"]
            unidad = leer_unidad(unidades_validas, prompt="Unidad (ej. KG, LT, M²): ")

            precio = leer_valor_numerico("Precio: ")
            peso = leer_valor_numerico("Peso: ")

            nuevo = Material(codigo, descripcion, unidad, precio, peso)

            with sqlite3.connect(self.nombre_db) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO datos (codigo, descripcion, unidad, precio, peso)
                    VALUES (?, ?, ?, ?, ?)
                """, (nuevo.codigo, nuevo.descripcion, nuevo.unidad, nuevo.precio, nuevo.peso))
                conn.commit()

            print("✅ Material agregado con éxito.")

        def agregar_material_manual(self, codigo, descripcion, unidad, precio, peso):
            with sqlite3.connect(self.nombre_db) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO datos (codigo, descripcion, unidad, precio, peso)
                    VALUES (?, ?, ?, ?, ?)
                """, (codigo, descripcion, unidad, precio, peso))
                conn.commit()


        def ver_datos(self):
            with sqlite3.connect(self.nombre_db) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM datos")
                datos = cursor.fetchall()
                return datos

            if not datos:
                console.print("⚠️ [yellow]No hay datos registrados.[/yellow]")
                return

            tabla = Table(title="📦 Lista de datos")
            tabla.add_column("Código", style="cyan")
            tabla.add_column("Descripción", style="white")
            tabla.add_column("Unidad", style="magenta")
            tabla.add_column("Precio", style="green", justify="right")
            tabla.add_column("Peso", style="blue", justify="right")

            for m in datos:
                tabla.add_row(m[0], m[1], m[2], f"${m[3]:,.2f}", str(m[4]))

            console.print(tabla)

# ------------------ GESTOR DE MANO DE OBRA ------------------

class GestorManoObraSQLite(GestorBaseSQLite):
    def __init__(self, nombre_db):
        campos = ["codigo", "descripcion", "unidad", "precio"]
        super().__init__(nombre_db, "mano_obra", campos)

    def crear_tabla(self):
        with sqlite3.connect(self.nombre_db) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS mano_obra (
                    codigo TEXT PRIMARY KEY,
                    descripcion TEXT NOT NULL,
                    unidad TEXT NOT NULL,
                    precio REAL NOT NULL
                )
            ''')
            conn.commit()

    def _existe_codigo(self, codigo):
        with sqlite3.connect(self.nombre_db) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT codigo FROM mano_obra WHERE codigo = ?", (codigo,))
            return cursor.fetchone() is not None


    def exportar_csv(self, archivo_csv="mano_obra_exportado.csv"):
        try:
            conexion = sqlite3.connect(self.nombre_base)
            cursor = conexion.cursor()
            cursor.execute("SELECT codigo, descripcion, unidad, valor_unitario FROM mano_obra")
            registros = cursor.fetchall()
            with open(archivo_csv, mode="w", newline="", encoding="utf-8") as archivo:
                writer = csv.writer(archivo)
                writer.writerow(["Código", "Descripción", "Unidad", "Valor Unitario"])
                writer.writerows(registros)
            print(f"📤 Mano de obra exportada a {archivo_csv}")
        except Exception as e:
            print(f"❌ Error al exportar mano de obra: {e}")
        finally:
            conexion.close()

    def agregar_mano_obra(self):
        print("\n🟢 Agregar mano de obra")
        codigo = leer_codigo("Código mobra: ", self._existe_codigo)
        descripcion = leer_descripcion("Descripción: ")

        unidades_validas = ["HH", "DD", "JN", "MS", "HN"]
        unidad = leer_unidad(unidades_validas, prompt="Unidad (HH, DD, JN, MS, HN): ")

        precio = leer_valor_numerico("Precio: ")

        with sqlite3.connect(self.nombre_db) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO mano_obra (codigo, descripcion, unidad, precio)
                VALUES (?, ?, ?, ?)
            """, (codigo, descripcion, unidad, precio))
            conn.commit()

        print("✅ Trabajador agregado con éxito.")

    def ver_mano_obra(self):
        with sqlite3.connect(self.nombre_db) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM mano_obra")
            trabajadores = cursor.fetchall()

        if not trabajadores:
            console.print("⚠️ [yellow]No hay trabajadores registrados.[/yellow]")
            return

        tabla = Table(title="🧑‍🔧 Mano de Obra")
        tabla.add_column("Código", style="cyan")
        tabla.add_column("Descripción", style="white")
        tabla.add_column("Unidad", style="magenta")
        tabla.add_column("Precio", style="green", justify="right")

        for t in trabajadores:
            tabla.add_row(t[0], t[1], t[2], f"${t[3]:,.2f}")

        console.print(tabla)

# ------------------ GESTOR DE HERRAMIENTAS ------------------

class GestorHerramientasSQLite(GestorBaseSQLite):
    def __init__(self, nombre_db):
        campos = ["codigo", "descripcion", "unidad", "precio"]
        super().__init__(nombre_db, "herramientas", campos)

    def crear_tabla(self):
        with sqlite3.connect(self.nombre_db) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS herramientas (
                    codigo TEXT PRIMARY KEY,
                    descripcion TEXT NOT NULL,
                    unidad TEXT NOT NULL,
                    precio REAL NOT NULL
                )
            ''')
            conn.commit()

    def _existe_codigo(self, codigo):
        with sqlite3.connect(self.nombre_db) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT codigo FROM herramientas WHERE codigo = ?", (codigo,))
            return cursor.fetchone() is not None



    def exportar_csv(self, archivo_csv="herramientas_exportado.csv"):
        try:
            conexion = sqlite3.connect(self.nombre_base)
            cursor = conexion.cursor()
            cursor.execute("SELECT codigo, descripcion, unidad, valor_unitario FROM herramientas")
            registros = cursor.fetchall()
            with open(archivo_csv, mode="w", newline="", encoding="utf-8") as archivo:
                writer = csv.writer(archivo)
                writer.writerow(["Código", "Descripción", "Unidad", "Valor Unitario"])
                writer.writerows(registros)
            print(f"📤 Herramientas exportadas a {archivo_csv}")
        except Exception as e:
            print(f"❌ Error al exportar herramientas: {e}")
        finally:
            conexion.close()



    def agregar_herramienta(self):
        print("\n🛠️ Agregar herramienta")
        codigo = leer_codigo("Código herramienta: ", self._existe_codigo)
        descripcion = leer_descripcion("Descripción: ")

        unidades_validas = ["DD", "MS", "HR","UN"]
        unidad = leer_unidad(unidades_validas, prompt="Unidad (UN, DD, MS, HR): ")

        precio = leer_valor_numerico("Precio: ")

        with sqlite3.connect(self.nombre_db) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO herramientas (codigo, descripcion, unidad, precio)
                VALUES (?, ?, ?, ?)
            """, (codigo, descripcion, unidad, precio))
            conn.commit()

        print("✅ Herramienta agregada con éxito.")

    def ver_herramientas(self):
        with sqlite3.connect(self.nombre_db) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM herramientas")
            herramientas = cursor.fetchall()

        if not herramientas:
            console.print("⚠️ [yellow]No hay herramientas registradas.[/yellow]")
            return

        tabla = Table(title="🛠️ Lista de Herramientas")
        tabla.add_column("Código", style="cyan")
        tabla.add_column("Descripción", style="white")
        tabla.add_column("Unidad", style="magenta")
        tabla.add_column("Precio", style="green", justify="right")

        for h in herramientas:
            tabla.add_row(h[0], h[1], h[2], f"${h[3]:,.2f}")

        console.print(tabla)

# ------------------ GESTOR DE TRANSPORTE ------------------

class GestorTransporteSQLite(GestorBaseSQLite):
    def __init__(self, nombre_db):
        campos = ["codigo", "descripcion", "unidad", "precio"]
        super().__init__(nombre_db, "transporte", campos)

    def crear_tabla(self):
        with sqlite3.connect(self.nombre_db) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS transporte (
                    codigo TEXT PRIMARY KEY,
                    descripcion TEXT NOT NULL,
                    unidad TEXT NOT NULL,
                    precio REAL NOT NULL
                )
            ''')
            conn.commit()

    def _existe_codigo(self, codigo):
        with sqlite3.connect(self.nombre_db) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT codigo FROM transporte WHERE codigo = ?", (codigo,))
            return cursor.fetchone() is not None


    def exportar_csv(self, archivo_csv="transporte_exportado.csv"):
        try:
            conexion = sqlite3.connect(self.nombre_base)
            cursor = conexion.cursor()
            cursor.execute("SELECT codigo, descripcion, unidad, precio FROM transporte")
            registros = cursor.fetchall()
            with open(archivo_csv, mode="w", newline="", encoding="utf-8") as archivo:
                writer = csv.writer(archivo)
                writer.writerow(["Código", "Descripción", "Unidad", "Precio"])
                writer.writerows(registros)
            print(f"📤 Transporte exportado a {archivo_csv}")
        except Exception as e:
            print(f"❌ Error al exportar transporte: {e}")
        finally:
            conexion.close()

    def agregar_transporte(self):
        print("\n🚚 Agregar transporte")
        codigo = leer_codigo("Código transporte: ", self._existe_codigo)
        descripcion = leer_descripcion("Descripción: ")

        unidades_validas = ["TK", "VJ", "M³", "MS", "DD", "HR","VK"]
        unidad = leer_unidad(unidades_validas, prompt="Unidad (TK, VJ, M³, MS, DD, HR): ")

        precio = leer_valor_unitario("Precio: ")

        with sqlite3.connect(self.nombre_db) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO transporte (codigo, descripcion, unidad, precio)
                VALUES (?, ?, ?, ?)
            """, (codigo, descripcion, unidad, precio))
            conn.commit()

        print("✅ Transporte agregado con éxito.")

    def ver_transporte(self):
        with sqlite3.connect(self.nombre_db) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM transporte")
            transportes = cursor.fetchall()

        if not transportes:
            console.print("⚠️ [yellow]No hay transportes registrados.[/yellow]")
            return

        tabla = Table(title="🚚 Lista de Transporte")
        tabla.add_column("Código", style="cyan")
        tabla.add_column("Descripción", style="white")
        tabla.add_column("Unidad", style="magenta")
        tabla.add_column("Precio", style="green", justify="right")

        for t in transportes:
            tabla.add_row(t[0], t[1], t[2], f"${t[3]:,.2f}")

        console.print(tabla)