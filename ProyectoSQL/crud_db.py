# crud_db.py
# crud_db.py
import mysql.connector
from mysql.connector import errorcode, Error
from crear_tablas import DB_CONFIG, DB_NAME

def get_connection():
    """Establece y retorna la conexión a la base de datos MySQL."""
    try:
        connection = mysql.connector.connect(database=DB_NAME, **DB_CONFIG)
        return connection
    except Error as e:
        if e.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("❌ Error: Usuario o contraseña incorrectos.")
        elif e.errno == errorcode.ER_BAD_DB_ERROR:
            print("❌ Error: La base de datos no existe.")
        else:
            print(f"❌ Error al conectar a la base de datos: {e}")
        return None

# ====================================================================
# --- Funciones CRUD para la tabla de materiales ---
# ====================================================================
def crear_material(codigo, descripcion, unidad, precio, peso, tipo):
    connection = get_connection()
    if connection is None:
        return
    cursor = connection.cursor()
    try:
        query = "INSERT INTO materiales (codigo, descripcion, unidad, precio, peso, tipo) VALUES (%s, %s, %s, %s, %s, %s)"
        data = (codigo, descripcion, unidad, precio, peso, tipo)
        cursor.execute(query, data)
        connection.commit()
    except Error as e:
        print(f"Error al crear material: {e}")
        raise e
    finally:
        cursor.close()
        connection.close()

def leer_materiales():
    connection = get_connection()
    if connection is None:
        return []
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM materiales")
        materiales = cursor.fetchall()
        return materiales
    except Error as e:
        print(f"Error al leer materiales: {e}")
        return []
    finally:
        cursor.close()
        connection.close()

def actualizar_material(codigo, nueva_descripcion, nueva_unidad, nuevo_precio, nuevo_peso, nuevo_tipo):
    connection = get_connection()
    if connection is None:
        return
    cursor = connection.cursor()
    try:
        query = """
            UPDATE materiales SET
                descripcion = %s,
                unidad = %s,
                precio = %s,
                peso = %s,
                tipo = %s
            WHERE codigo = %s
        """
        data = (nueva_descripcion, nueva_unidad, nuevo_precio, nuevo_peso, nuevo_tipo, codigo)
        cursor.execute(query, data)
        connection.commit()
    except Error as e:
        print(f"Error al actualizar material: {e}")
        raise e
    finally:
        cursor.close()
        connection.close()

# ====================================================================
# --- Funciones CRUD para la tabla de mano de obra ---
# ====================================================================
def crear_mobra(codigo, descripcion, unidad, precio):
    connection = get_connection()
    if connection is None:
        return
    cursor = connection.cursor()
    try:
        query = "INSERT INTO mobra (codigo, descripcion, unidad, precio) VALUES (%s, %s, %s, %s)"
        data = (codigo, descripcion, unidad, precio)
        cursor.execute(query, data)
        connection.commit()
    except Error as e:
        print(f"Error al crear mano de obra: {e}")
        raise e
    finally:
        cursor.close()
        connection.close()

def leer_mobra():
    connection = get_connection()
    if connection is None:
        return []
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM mobra")
        mobra = cursor.fetchall()
        return mobra
    except Error as e:
        print(f"Error al leer mano de obra: {e}")
        return []
    finally:
        cursor.close()
        connection.close()

def actualizar_mobra(codigo, nueva_descripcion, nueva_unidad, nuevo_precio):
    connection = get_connection()
    if connection is None:
        return
    cursor = connection.cursor()
    try:
        query = """
            UPDATE mobra SET
                descripcion = %s,
                unidad = %s,
                precio = %s
            WHERE codigo = %s
        """
        data = (nueva_descripcion, nueva_unidad, nuevo_precio, codigo)
        cursor.execute(query, data)
        connection.commit()
    except Error as e:
        print(f"Error al actualizar mano de obra: {e}")
        raise e
    finally:
        cursor.close()
        connection.close()

# ====================================================================
# --- Funciones CRUD para la tabla de herramientas ---
# ====================================================================
def crear_herramienta(codigo, descripcion, unidad, precio):
    connection = get_connection()
    if connection is None:
        return
    cursor = connection.cursor()
    try:
        query = "INSERT INTO herramienta (codigo, descripcion, unidad, precio) VALUES (%s, %s, %s, %s)"
        data = (codigo, descripcion, unidad, precio)
        cursor.execute(query, data)
        connection.commit()
    except Error as e:
        print(f"Error al crear herramienta: {e}")
        raise e
    finally:
        cursor.close()
        connection.close()

def leer_herramientas():
    connection = get_connection()
    if connection is None:
        return []
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM herramienta")
        herramientas = cursor.fetchall()
        return herramientas
    except Error as e:
        print(f"Error al leer herramientas: {e}")
        return []
    finally:
        cursor.close()
        connection.close()

def actualizar_herramienta(codigo, nueva_descripcion, nueva_unidad, nuevo_precio):
    connection = get_connection()
    if connection is None:
        return
    cursor = connection.cursor()
    try:
        query = """
            UPDATE herramienta SET
                descripcion = %s,
                unidad = %s,
                precio = %s
            WHERE codigo = %s
        """
        data = (nueva_descripcion, nueva_unidad, nuevo_precio, codigo)
        cursor.execute(query, data)
        connection.commit()
    except Error as e:
        print(f"Error al actualizar herramienta: {e}")
        raise e
    finally:
        cursor.close()
        connection.close()

# ====================================================================
# --- Funciones CRUD para la tabla de transporte ---
# ====================================================================
def crear_transporte(codigo, descripcion, unidad, precio):
    connection = get_connection()
    if connection is None:
        return
    cursor = connection.cursor()
    try:
        query = "INSERT INTO transporte (codigo, descripcion, unidad, precio) VALUES (%s, %s, %s, %s)"
        data = (codigo, descripcion, unidad, precio)
        cursor.execute(query, data)
        connection.commit()
    except Error as e:
        print(f"Error al crear transporte: {e}")
        raise e
    finally:
        cursor.close()
        connection.close()

def leer_transporte():
    connection = get_connection()
    if connection is None:
        return []
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM transporte")
        transporte = cursor.fetchall()
        return transporte
    except Error as e:
        print(f"Error al leer transporte: {e}")
        return []
    finally:
        cursor.close()
        connection.close()

def actualizar_transporte(codigo, nueva_descripcion, nueva_unidad, nuevo_precio):
    connection = get_connection()
    if connection is None:
        return
    cursor = connection.cursor()
    try:
        query = """
            UPDATE transporte SET
                descripcion = %s,
                unidad = %s,
                precio = %s
            WHERE codigo = %s
        """
        data = (nueva_descripcion, nueva_unidad, nuevo_precio, codigo)
        cursor.execute(query, data)
        connection.commit()
    except Error as e:
        print(f"Error al actualizar transporte: {e}")
        raise e
    finally:
        cursor.close()
        connection.close()

# ====================================================================
# --- Funciones para la tabla de análisis unitario ---
# ====================================================================
def crear_unitario(codigo, descripcion, unidad):
    connection = get_connection()
    if connection is None:
        return
    cursor = connection.cursor()
    try:
        query = "INSERT INTO unitario (codigo, descripcion, unidad) VALUES (%s, %s, %s)"
        data = (codigo, descripcion, unidad)
        cursor.execute(query, data)
        connection.commit()
    except Error as e:
        print(f"Error al crear unitario: {e}")
        raise e
    finally:
        cursor.close()
        connection.close()

def leer_unitarios():
    connection = get_connection()
    if connection is None:
        return []
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM unitario")
        unitarios = cursor.fetchall()
        return unitarios
    except Error as e:
        print(f"Error al leer unitarios: {e}")
        return []
    finally:
        cursor.close()
        connection.close()

def crear_componente_unitario(codigo_unitario, tipo_componente, codigo_componente, cantidad):
    connection = get_connection()
    if connection is None:
        return
    cursor = connection.cursor()
    try:
        # Mapeo del tipo de componente a la tabla correspondiente
        if tipo_componente == 'material':
            tabla = 'unitario_materiales'
            col_codigo = 'codigo_material'
        elif tipo_componente == 'mobra':
            tabla = 'unitario_mobra'
            col_codigo = 'codigo_mobra'
        elif tipo_componente == 'herramienta':
            tabla = 'unitario_herramienta'
            col_codigo = 'codigo_herramienta'
        elif tipo_componente == 'transporte':
            tabla = 'unitario_transporte'
            col_codigo = 'codigo_transporte'
        else:
            raise ValueError("Tipo de componente no válido.")

        query = f"INSERT INTO {tabla} (codigo_unitario, {col_codigo}, cantidad) VALUES (%s, %s, %s)"
        data = (codigo_unitario, codigo_componente, cantidad)
        cursor.execute(query, data)
        connection.commit()
    except Error as e:
        print(f"Error al crear componente de unitario: {e}")
        raise e
    except ValueError as e:
        print(f"Error: {e}")
        raise e
    finally:
        cursor.close()
        connection.close()
        
def leer_componentes_unitario(codigo_unitario):
    connection = get_connection()
    if connection is None:
        return {}
    cursor = connection.cursor()
    componentes = {
        "material": [],
        "mobra": [],
        "herramienta": [],
        "transporte": []
    }
    
    tablas = {
        "material": "unitario_materiales",
        "mobra": "unitario_mobra",
        "herramienta": "unitario_herramienta",
        "transporte": "unitario_transporte"
    }

    try:
        for tipo, tabla_relacional in tablas.items():
            query_join = f"""
                SELECT c.cantidad, item.*
                FROM {tabla_relacional} c
                JOIN {tipo} item ON c.codigo_{tipo} = item.codigo
                WHERE c.codigo_unitario = %s
            """
            cursor.execute(query_join, (codigo_unitario,))
            items = cursor.fetchall()
            
            for item in items:
                # La cantidad es el primer elemento del resultado del JOIN
                cantidad = item[0]
                # El resto de los elementos son los datos del item (código, descripción, etc.)
                item_data = item[1:]
                
                # Insertar en el diccionario, ajustando la tupla según el tipo
                if tipo == 'material':
                    # material tiene 6 campos, el resultado es (cantidad, codigo, desc, unidad, precio, peso, tipo)
                    componentes[tipo].append((item_data[0], item_data[1], item_data[2], item_data[3], item_data[4], cantidad))
                else:
                    # los otros tienen 4 campos, el resultado es (cantidad, codigo, desc, unidad, precio)
                    componentes[tipo].append((item_data[0], item_data[1], item_data[2], item_data[3], cantidad))
                    
    except Error as e:
        print(f"Error al leer componentes de unitario: {e}")
        return {}
    finally:
        cursor.close()
        connection.close()
        
    return componentes