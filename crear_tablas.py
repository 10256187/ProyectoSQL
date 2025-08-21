import mysql.connector
from mysql.connector import errorcode, Error

# --- 1. Configuración de la conexión a la base de datos ---
DB_CONFIG = {
    'user': 'root',
    'password': '123@Chepe$#',
    'host': 'localhost'
}

DB_NAME = 'ProyectoSQL'

# --- 2. Sentencias SQL de las tablas ---
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
    )
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
    )
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
    )
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
    )
    """,
    """
        -- ========================================
    -- TABLA PRINCIPAL UNITARIO
    -- ========================================
    CREATE TABLE IF NOT EXISTS unitario (
        codigo VARCHAR(9) PRIMARY KEY,
        descripcion VARCHAR(255) NOT NULL,
        unidad VARCHAR(3) NOT NULL,
        CONSTRAINT chk_unitario_unidad_valida
            CHECK (unidad IN ('UN','ML','KM','LB','KG','TN','SC','GL','GB','PG','M2','M3','Lt')),
        CONSTRAINT chk_unitario_codigo_formato
            CHECK (codigo REGEXP '^[A-Z]{4}-[0-9]{4}$')
    )
    """,
    """
    -- ========================================
    -- TABLAS DE DETALLE
    -- Se ha eliminado la columna 'id' y se ha corregido el diseño para
    -- que cada tabla use un índice compuesto como clave primaria.
    -- ========================================

    -- 1. Materiales
    CREATE TABLE IF NOT EXISTS unitario_material (
        codigo_unitario VARCHAR(9) NOT NULL,
        codigo_componente VARCHAR(9) NOT NULL,
        cantidad DECIMAL(10,2) NOT NULL,
        PRIMARY KEY (codigo_unitario, codigo_componente),
        FOREIGN KEY (codigo_unitario) REFERENCES unitario(codigo)
            ON DELETE CASCADE ON UPDATE CASCADE,
        FOREIGN KEY (codigo_componente) REFERENCES materiales(codigo)
            ON DELETE CASCADE ON UPDATE CASCADE
    )
    """,
    """
    -- 2. Mano de Obra
    CREATE TABLE IF NOT EXISTS unitario_mano_obra (
        codigo_unitario VARCHAR(9) NOT NULL,
        codigo_componente VARCHAR(9) NOT NULL,
        cantidad DECIMAL(10,2) NOT NULL,
        PRIMARY KEY (codigo_unitario, codigo_componente),
        FOREIGN KEY (codigo_unitario) REFERENCES unitario(codigo)
            ON DELETE CASCADE ON UPDATE CASCADE,
        FOREIGN KEY (codigo_componente) REFERENCES mobra(codigo)
            ON DELETE CASCADE ON UPDATE CASCADE
    )
    """,
    """
    -- 3. Herramientas
    CREATE TABLE IF NOT EXISTS unitario_herramienta (
        codigo_unitario VARCHAR(9) NOT NULL,
        codigo_componente VARCHAR(9) NOT NULL,
        cantidad DECIMAL(10,2) NOT NULL,
        PRIMARY KEY (codigo_unitario, codigo_componente),
        FOREIGN KEY (codigo_unitario) REFERENCES unitario(codigo)
            ON DELETE CASCADE ON UPDATE CASCADE,
        FOREIGN KEY (codigo_componente) REFERENCES herramienta(codigo)
            ON DELETE CASCADE ON UPDATE CASCADE
    )
    """,
    """
    -- 4. Transporte
    CREATE TABLE IF NOT EXISTS unitario_transporte (
        codigo_unitario VARCHAR(9) NOT NULL,
        codigo_componente VARCHAR(9) NOT NULL,
        cantidad DECIMAL(10,2) NOT NULL,
        PRIMARY KEY (codigo_unitario, codigo_componente),
        FOREIGN KEY (codigo_unitario) REFERENCES unitario(codigo)
            ON DELETE CASCADE ON UPDATE CASCADE,
        FOREIGN KEY (codigo_componente) REFERENCES transporte(codigo)
            ON DELETE CASCADE ON UPDATE CASCADE
    )
    """
]

def create_database_and_tables():
    try:
        # 1. Crear la base de datos
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        print(f"✅ Base de datos '{DB_NAME}' creada/verificada.")
        cursor.close()
        connection.close()

        # 2. Conectarse directamente a la base de datos
        connection = mysql.connector.connect(database=DB_NAME, **DB_CONFIG)
        cursor = connection.cursor()

        # 3. Crear las tablas
        for ddl in sql_tablas:
            try:
                cursor.execute(ddl)
            except Error as err:
                print(f"❌ Error ejecutando tabla: {err}")
        connection.commit()
        print("🎉 Todas las tablas fueron creadas/verificadas.")

    except Error as e:
        if e.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("❌ Error: Usuario o contraseña incorrectos.")
        elif e.errno == errorcode.ER_BAD_DB_ERROR:
            print("❌ Error: La base de datos no existe.")
        else:
            print(f"❌ Error inesperado: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("🔌 Conexión cerrada.")

if __name__ == '__main__':
    create_database_and_tables()