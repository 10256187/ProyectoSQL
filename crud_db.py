# crud_db.py - Versión actualizada
import mysql.connector
from mysql.connector import errorcode, Error
import re
import sys

# --- 1. Configuración de la conexión a la base de datos ---
DB_CONFIG = {
    'user': 'root',
    'password': '123@Chepe$#', 
    'host': 'localhost',
    'database': 'ProyectoSQL'
}

# --- 2. Funciones de la base de datos ---

def get_db_connection():
    """
    Establece y retorna una conexión a la base de datos.
    Retorna None en caso de error.
    """
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        create_tables(connection)
        return connection
    except Error as e:
        print(f"❌ Error al conectar a la base de datos: {e}")
        return None

def close_db_connection(connection):
    """
    Cierra la conexión a la base de datos si está abierta.
    """
    if connection and connection.is_connected():
        connection.close()
        
def create_tables(connection):
    """
    Crea las tablas necesarias si no existen.
    """
    cursor = connection.cursor()
    
    # Sentencias SQL de las tablas
    sql_tablas = [
        """
        CREATE TABLE IF NOT EXISTS materiales (
            codigo VARCHAR(9) PRIMARY KEY,
            descripcion VARCHAR(255) NOT NULL,
            unidad VARCHAR(3) NOT NULL,
            precio DECIMAL(10, 2) NOT NULL,
            peso DECIMAL(10, 2),
            tipo VARCHAR(3) NOT NULL,
            CONSTRAINT chk_materiales_unidad_valida CHECK (unidad IN ('UN','ML','KM','LB','KG','TN','SC','GL','GB','PG','M2','M3','Lt')),
            CONSTRAINT chk_materiales_precio_positivo CHECK (precio >= 0),
            CONSTRAINT chk_materiales_peso_positivo CHECK (peso >= 0),
            CONSTRAINT chk_materiales_tipo_valido CHECK (tipo IN ('MAR','HIE','CEM','CON','HER','CAB','ESM','ESC','ELE','ILU','CPM','CAP')),
            CONSTRAINT chk_materiales_codigo_formato CHECK (codigo REGEXP '^[A-Z]{4}-[0-9]{4}$')
        ) ENGINE=InnoDB;
        """,
        """
        CREATE TABLE IF NOT EXISTS mobra (
            codigo VARCHAR(9) PRIMARY KEY,
            descripcion VARCHAR(255) NOT NULL,
            unidad VARCHAR(2) NOT NULL,
            precio DECIMAL(10, 2) NOT NULL,
            CONSTRAINT chk_mobra_unidad_valida CHECK (unidad IN ('HH','DD','MS','JN','VT','CM')),
            CONSTRAINT chk_mobra_precio_positivo CHECK (precio >= 0),
            CONSTRAINT chk_mobra_codigo_formato CHECK (codigo REGEXP '^[A-Z]{4}-[0-9]{4}$')
        ) ENGINE=InnoDB;
        """,
        """
        CREATE TABLE IF NOT EXISTS herramienta (
            codigo VARCHAR(9) PRIMARY KEY,
            descripcion VARCHAR(255) NOT NULL,
            unidad VARCHAR(3) NOT NULL,
            precio DECIMAL(10, 2) NOT NULL,
            CONSTRAINT chk_herramienta_unidad_valida CHECK (unidad IN ('HR','DD','MS','VJ','M³')),
            CONSTRAINT chk_herramienta_precio_positivo CHECK (precio >= 0),
            CONSTRAINT chk_herramienta_codigo_formato CHECK (codigo REGEXP '^[A-Z]{4}-[0-9]{4}$')
        ) ENGINE=InnoDB;
        """,
        """
        CREATE TABLE IF NOT EXISTS transporte (
            codigo VARCHAR(9) PRIMARY KEY,
            descripcion VARCHAR(255) NOT NULL,
            unidad VARCHAR(3) NOT NULL,
            precio DECIMAL(10, 2) NOT NULL,
            CONSTRAINT chk_transporte_unidad_valida CHECK (unidad IN ('VJ','M³','MS','DD','HR','TKM')),
            CONSTRAINT chk_transporte_precio_positivo CHECK (precio >= 0),
            CONSTRAINT chk_transporte_codigo_formato CHECK (codigo REGEXP '^[A-Z]{4}-[0-9]{4}$')
        ) ENGINE=InnoDB;
        """,
        """
        CREATE TABLE IF NOT EXISTS unitario (
            codigo VARCHAR(9) PRIMARY KEY,
            descripcion VARCHAR(255) NOT NULL,
            unidad VARCHAR(3) NOT NULL,
            CONSTRAINT chk_unitario_unidad_valida
                CHECK (unidad IN ('UN','ML','KM','LB','KG','TN','SC','GL','GB','PG','M2','M3','Lt')),
            CONSTRAINT chk_unitario_codigo_formato
                CHECK (codigo REGEXP '^[A-Z]{4}-[0-9]{4}$')
        ) ENGINE=InnoDB;
        """,
        """
        CREATE TABLE IF NOT EXISTS unitario_material (
            codigo_unitario VARCHAR(9) NOT NULL,
            codigo_componente VARCHAR(9) NOT NULL,
            cantidad DECIMAL(10,2) NOT NULL,
            PRIMARY KEY (codigo_unitario, codigo_componente),
            FOREIGN KEY (codigo_unitario) REFERENCES unitario(codigo)
                ON DELETE CASCADE ON UPDATE CASCADE,
            FOREIGN KEY (codigo_componente) REFERENCES materiales(codigo)
                ON DELETE CASCADE ON UPDATE CASCADE
        ) ENGINE=InnoDB;
        """,
        """
        CREATE TABLE IF NOT EXISTS unitario_mano_obra (
            codigo_unitario VARCHAR(9) NOT NULL,
            codigo_componente VARCHAR(9) NOT NULL,
            cantidad DECIMAL(10,2) NOT NULL,
            PRIMARY KEY (codigo_unitario, codigo_componente),
            FOREIGN KEY (codigo_unitario) REFERENCES unitario(codigo)
                ON DELETE CASCADE ON UPDATE CASCADE,
            FOREIGN KEY (codigo_componente) REFERENCES mobra(codigo)
                ON DELETE CASCADE ON UPDATE CASCADE
        ) ENGINE=InnoDB;
        """,
        """
        CREATE TABLE IF NOT EXISTS unitario_herramienta (
            codigo_unitario VARCHAR(9) NOT NULL,
            codigo_componente VARCHAR(9) NOT NULL,
            cantidad DECIMAL(10,2) NOT NULL,
            PRIMARY KEY (codigo_unitario, codigo_componente),
            FOREIGN KEY (codigo_unitario) REFERENCES unitario(codigo)
                ON DELETE CASCADE ON UPDATE CASCADE,
            FOREIGN KEY (codigo_componente) REFERENCES herramienta(codigo)
                ON DELETE CASCADE ON UPDATE CASCADE
        ) ENGINE=InnoDB;
        """,
        """
        CREATE TABLE IF NOT EXISTS unitario_transporte (
            codigo_unitario VARCHAR(9) NOT NULL,
            codigo_componente VARCHAR(9) NOT NULL,
            cantidad DECIMAL(10,2) NOT NULL,
            PRIMARY KEY (codigo_unitario, codigo_componente),
            FOREIGN KEY (codigo_unitario) REFERENCES unitario(codigo)
                ON DELETE CASCADE ON UPDATE CASCADE,
            FOREIGN KEY (codigo_componente) REFERENCES transporte(codigo)
                ON DELETE CASCADE ON UPDATE CASCADE
        ) ENGINE=InnoDB;
        """
    ]
    
    try:
        print("Creando tablas si no existen...")
        for ddl in sql_tablas:
            cursor.execute(ddl)
        connection.commit()
        print("Tablas verificadas/creadas correctamente.")
    except mysql.connector.Error as err:
        print(f"Error al crear las tablas: {err}")
    finally:
        cursor.close()

# --- 3. Funciones auxiliares ---

def format_item_code(code):
    """Formatea una cadena de código para que cumpla con el patrón 'AAAA-9999'."""
    if not isinstance(code, str):
        return None
    normalized_code = code.strip().replace('-', '').upper()
    if len(normalized_code) != 8 or not re.fullmatch(r'^[A-Z]{4}[0-9]{4}$', normalized_code):
        return None
    return f"{normalized_code[:4]}-{normalized_code[4:]}"

# --- 4. Funciones CRUD (Create, Read, Update, Delete) ---

def create_item(connection, table_name, data):
    """Función genérica para crear un nuevo registro en una tabla."""
    # La tabla unitario tiene su propia restricción de formato en la base de datos
    if 'codigo' in data and table_name != 'unitario':
        data['codigo'] = format_item_code(data['codigo'])
        if data['codigo'] is None:
            raise ValueError("Formato de código inválido.")
    
    cursor = connection.cursor()
    columns = ', '.join(data.keys())
    placeholders = ', '.join(['%s'] * len(data))
    query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
    values = tuple(data.values())
    try:
        cursor.execute(query, values)
        connection.commit()
        print(f"✅ Nuevo registro creado en '{table_name}'.")
    except Error as err:
        print(f"❌ Error al crear registro en '{table_name}': {err}")
        connection.rollback()
        raise err
    finally:
        cursor.close()

def read_all_items(connection, table_name):
    """Lee y retorna todos los registros de una tabla genérica."""
    cursor = connection.cursor(dictionary=True)
    query = f"SELECT * FROM {table_name}"
    try:
        cursor.execute(query)
        items = cursor.fetchall()
        return items
    except Error as err:
        print(f"❌ Error al leer la tabla '{table_name}': {err}")
        return []
    finally:
        cursor.close()

def read_item_by_code(connection, table_name, item_code):
    """Busca y retorna los detalles de un insumo específico por su código."""
    cursor = connection.cursor(dictionary=True)
    query = f"SELECT * FROM {table_name} WHERE codigo = %s"
    try:
        cursor.execute(query, (item_code,))
        result = cursor.fetchone()
        return result
    except Error as err:
        print(f"❌ Error al leer el insumo: {err}")
        return None
    finally:
        cursor.close()

def update_item(connection, table_name, data, condition):
    """Función genérica para actualizar un registro en una tabla."""
    cursor = connection.cursor()
    set_clause = ', '.join([f"{key} = %s" for key in data.keys()])
    where_clause = ' AND '.join([f"{key} = %s" for key in condition.keys()])
    query = f"UPDATE {table_name} SET {set_clause} WHERE {where_clause}"
    values = tuple(list(data.values()) + list(condition.values()))
    try:
        cursor.execute(query, values)
        connection.commit()
        print(f"✅ Registro en '{table_name}' actualizado.")
    except Error as err:
        print(f"❌ Error al actualizar registro en '{table_name}': {err}")
        connection.rollback()
        raise err
    finally:
        cursor.close()

def delete_item(connection, table_name, condition):
    """Función genérica para eliminar un registro en una tabla."""
    cursor = connection.cursor()
    where_clause = ' AND '.join([f"{key} = %s" for key in condition.keys()])
    query = f"DELETE FROM {table_name} WHERE {where_clause}"
    values = tuple(condition.values())
    try:
        cursor.execute(query, values)
        connection.commit()
        print(f"✅ Registro en '{table_name}' eliminado.")
    except Error as err:
        print(f"❌ Error al eliminar registro en '{table_name}': {err}")
        connection.rollback()
        raise err
    finally:
        cursor.close()

# --- 5. Funciones específicas para APUs y componentes ---

def read_all_apus(connection):
    """Lee y retorna todos los APU de la tabla 'unitario'."""
    return read_all_items(connection, 'unitario')

def read_apu_details(connection, codigo_apu):
    """
    Lee los detalles y componentes de un APU específico, adaptado a tu esquema.
    Ahora incluye el costo del componente (cantidad * precio).
    """
    details = {'components': {}}
    cursor = connection.cursor(dictionary=True)

    component_tables = {
        'materiales': 'unitario_material',
        'mobra': 'unitario_mano_obra',
        'herramienta': 'unitario_herramienta',
        'transporte': 'unitario_transporte'
    }

    try:
        for comp_type, table_name in component_tables.items():
            insumo_table = comp_type
            
            # Consulta SQL modificada para incluir el campo de costo_componente
            query = f"""
            SELECT '{comp_type}' AS tipo,
                   T1.codigo_componente AS codigo,
                   T2.descripcion,
                   T2.unidad,
                   T2.precio,
                   T1.cantidad,
                   (T2.precio * T1.cantidad) AS costo_componente
            FROM {table_name} T1
            JOIN {insumo_table} T2 ON T1.codigo_componente = T2.codigo
            WHERE T1.codigo_unitario = %s;
            """
            cursor.execute(query, (codigo_apu,))
            details['components'][comp_type] = cursor.fetchall()
            
    except mysql.connector.Error as err:
        print(f"Error al leer detalles del APU: {err}")
        details = None
    finally:
        cursor.close()
    return details

def add_component_to_apu(connection, apu_codigo, tipo_insumo, insumo_codigo, cantidad):
    """Añade un componente a un APU específico, adaptado a tu esquema."""
    # Mapea los nombres de tipo a los nombres de tabla correctos
    table_name_map = {
        'materiales': 'unitario_material',
        'mobra': 'unitario_mano_obra',
        'herramienta': 'unitario_herramienta',
        'transporte': 'unitario_transporte',
    }
    table_name = table_name_map.get(tipo_insumo)

    if not table_name:
        raise ValueError(f"Tipo de insumo desconocido: {tipo_insumo}")

    cursor = connection.cursor()
    # Usa tu formato de tabla (ej. unitario_material)
    query = f"INSERT INTO {table_name} (codigo_unitario, codigo_componente, cantidad) VALUES (%s, %s, %s)"
    
    # Formatear el código del componente antes de la inserción
    formatted_insumo_codigo = format_item_code(insumo_codigo)
    if not formatted_insumo_codigo:
        raise ValueError(f"Formato de código de componente inválido: {insumo_codigo}")
        
    values = (apu_codigo, formatted_insumo_codigo, cantidad)
    
    try:
        cursor.execute(query, values)
        connection.commit()
        print("Componente añadido al APU correctamente.")
    except Error as err:
        print(f"Error al añadir componente al APU: {err}")
        connection.rollback()
        raise err
    finally:
        cursor.close()

def update_apu(connection, apu_code, new_data):
    """
    Actualiza la información principal de un APU.
    Parámetros:
        connection: Objeto de conexión.
        apu_code: Código del APU a actualizar.
        new_data: Diccionario con los nuevos datos (ej. {'descripcion': 'Nueva descripción'}).
    """
    update_item(connection, 'unitario', new_data, {'codigo': apu_code})

def update_component_quantity(connection, apu_code, component_code, component_type, new_quantity):
    """
    Actualiza la cantidad de un componente en un APU.
    """
    table_name = f'unitario_{component_type}'
    update_item(
        connection, 
        table_name, 
        {'cantidad': new_quantity}, 
        {'codigo_unitario': apu_code, 'codigo_componente': component_code}
    )

def delete_apu(connection, apu_code):
    """
    Elimina un APU y sus componentes asociados (gracias a ON DELETE CASCADE).
    """
    delete_item(connection, 'unitario', {'codigo': apu_code})

def delete_component_from_apu(connection, apu_code, component_code, component_type):
    """
    Elimina un componente específico de un APU.
    """
    table_name = f'unitario_{component_type}'
    delete_item(
        connection, 
        table_name, 
        {'codigo_unitario': apu_code, 'codigo_componente': component_code}
    )

def calculate_apu_cost(connection, apu_code):
    """
    Calcula el costo total de un APU sumando el costo de todos sus componentes.
    """
    cursor = connection.cursor()
    total_cost = 0

    component_tables = {
        'materiales': 'unitario_material',
        'mobra': 'unitario_mano_obra',
        'herramienta': 'unitario_herramienta',
        'transporte': 'unitario_transporte'
    }
    
    try:
        for comp_type, rel_table in component_tables.items():
            insumo_table = comp_type
            
            query = f"""
                SELECT SUM(t2.precio * t1.cantidad)
                FROM {rel_table} t1
                JOIN {insumo_table} t2 ON t1.codigo_componente = t2.codigo
                WHERE t1.codigo_unitario = %s
            """
            cursor.execute(query, (apu_code,))
            result = cursor.fetchone()[0]
            if result is not None:
                total_cost += result
        return total_cost
    except Error as err:
        print(f"❌ Error al calcular el costo del APU: {err}")
        return 0
    finally:
        cursor.close()