import sqlite3

# Conexión con la base de datos
def conectar():
    return sqlite3.connect("materiales.db")

# Crear la tabla si no existe
def crear_tabla():
    conn = sqlite3.connect("materiales.db")
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
    conn.close()

# # --- FUNCIONES DE INGRESO Y VALIDACIÓN UNIFICADAS ---

def pedir_codigo(cursor, modo="nuevo", codigo_actual=None):
    """
    Valida y pide un código de material.
    
    - modo="nuevo": el código no debe existir en la base de datos.
    - modo="existente": el código debe existir en la base de datos.
    - codigo_actual: usado durante edición para permitir dejar el código sin cambiar.

    Devuelve:
        - Si modo="nuevo": un código válido y único
        - Si modo="existente": una tupla (código, material)
    """
    while True:
        entrada = input("Código (Ej: CCUD0001): ").strip().upper().replace("-", "")
        
        # Si se deja en blanco y es una edición, se conserva el anterior
        if not entrada and codigo_actual:
            return codigo_actual if modo == "nuevo" else (codigo_actual, None)

        if len(entrada) == 8 and entrada[:4].isalpha() and entrada[4:].isdigit():
            codigo_formateado = f"{entrada[:4]}-{entrada[4:]}"
            
            cursor.execute("SELECT * FROM materiales WHERE codigo = ?", (codigo_formateado,))
            material = cursor.fetchone()

            if modo == "nuevo":
                if material and codigo_formateado != codigo_actual:
                    print(f"❌ El código '{codigo_formateado}' ya existe. No se puede duplicar.")
                else:
                    return codigo_formateado
            elif modo == "existente":
                if material:
                    return codigo_formateado, material
                else:
                    print(f"❌ El código '{codigo_formateado}' no existe en la base de datos.")
        else:
            print("❌ El código debe tener 4 letras seguidas de 4 números (Ej: CCUD0001)")

def pedir_unidad(unidad_actual=None):
    unidades_validas = {"ML", "kG", "UN", "LT", "MT", "M²", "M³","SC","GL", "LB", "kM","kW"}
    while True:
        entrada = input(f"Unidad ({', '.join(unidades_validas)}): ").strip().upper()
        if not entrada and unidad_actual:
            return unidad_actual
        if len(entrada) == 2 and entrada[0].isalpha() and entrada in unidades_validas:
            return entrada
        print("❌ Unidad inválida. Usa una válida de la lista.")

def pedir_float(texto, valor_actual=None):
    while True:
        entrada = input(f"{texto}: ").strip().replace(",", ".")
        if not entrada and valor_actual is not None:
            return valor_actual
        try:
            return float(entrada)
        except ValueError:
            print("❌ Debe ingresar un número válido.")

def pedir_descripcion(descripcion_actual=None):
    entrada = input("Descripción: ").strip()
    return entrada if entrada else descripcion_actual

# Agregar un nuevo insumo con validaciones
def agregar_insumo(cursor, conexion):
    print("\n🟢 Agregar nuevo insumo")

    # Paso 1: Validaciones
    codigo = codigo = pedir_codigo(cursor, modo="nuevo")
    descripcion = pedir_descripcion()
    unidad = pedir_unidad(unidad_actual=None)
    precio = pedir_float("Precio")
    peso = pedir_float("Peso")

    # Paso 2: Inserción en la base de datos
    try:
        cursor.execute("""
            INSERT INTO materiales (codigo, descripcion, unidad, precio, peso)
            VALUES (?, ?, ?, ?, ?)
        """, (codigo, descripcion, unidad, precio, peso))
        conexion.commit()
        print(f"✅ Insumo '{codigo}' agregado correctamente.")
    except Exception as e:
        print(f"❌ Error al guardar en la base de datos: {e}")

    # Ver todos los materiales
def ver_materiales():
    print("\n📋 Lista de materiales registrados:")
    conn = sqlite3.connect("materiales.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM materiales ORDER BY codigo")
    registros = cursor.fetchall()
    if not registros:
        print("⚠️ No hay materiales registrados.")
    for r in registros:
        print(f"- {r[0]} | {r[1]} | {r[2]} | ${r[3]} | {r[4]}kg")
    conn.close()

# Edición de Insumos
def editar_material():
    import sqlite3

    conexion = sqlite3.connect("materiales.db")
    cursor = conexion.cursor()

    codigo, material = pedir_codigo(cursor, modo="existente")

    cursor.execute("SELECT * FROM materiales WHERE codigo = ?", (codigo,))
    material = cursor.fetchone()

    if not material:
        print("❌ No se encontró un material con ese código.")
        conexion.close()
        return

    print(f"✏️ Editando material: {material}")

    nueva_descripcion = input("Nueva descripción (deja en blanco para conservar): ").strip()
    nueva_unidad = input("Nueva unidad (deja en blanco para conservar): ").strip().upper()
    nuevo_precio = input("Nuevo precio (deja en blanco para conservar): ").strip()
    nuevo_peso = input("Nuevo peso (deja en blanco para conservar): ").strip()

    # Usamos los valores anteriores si se dejan en blanco
    descripcion = nueva_descripcion or material[1]
    unidad = nueva_unidad or material[2]
    precio = float(nuevo_precio.replace(",", ".")) if nuevo_precio else material[3]
    peso = float(nuevo_peso.replace(",", ".")) if nuevo_peso else material[4]

    cursor.execute("""
        UPDATE materiales
        SET descripcion = ?, unidad = ?, precio = ?, peso = ?
        WHERE codigo = ?
    """, (descripcion, unidad, precio, peso, codigo))

    conexion.commit()
    conexion.close()
    print("✅ Material actualizado correctamente.")

# Función para eliminar material de la base

def eliminar_material():
    print("\n🗑️ Eliminar material")

    conn = conectar()
    cursor = conn.cursor()

    # Usamos pedir_codigo en modo 'existente' para validar
    codigo, material = pedir_codigo(cursor, modo="existente")
    if not material:
        conn.close()
        return

    print(f"🔍 Material encontrado: {material[0]} | {material[1]} | {material[2]} | ${material[3]} | {material[4]}kg")

    confirmar = input("¿Estás seguro de que quieres eliminar este material? (S/N): ").strip().upper()
    if confirmar == "S":
        try:
            cursor.execute("DELETE FROM materiales WHERE codigo = ?", (codigo,))
            conn.commit()
            print(f"✅ Material '{codigo}' eliminado correctamente.")
        except Exception as e:
            print(f"❌ Error al eliminar: {e}")
    else:
        print("⛔ Operación cancelada por el usuario.")

    conn.close()