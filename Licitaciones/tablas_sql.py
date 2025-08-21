# tablas_sql.py

TABLAS_SQL = {
    "materiales": """
        CREATE TABLE IF NOT EXISTS materiales (
            codigo TEXT PRIMARY KEY,
            descripcion TEXT NOT NULL,
            unidad TEXT NOT NULL,
            precio REAL NOT NULL,
            peso REAL NOT NULL
        )
    """,
    "mano_obra": """
        CREATE TABLE IF NOT EXISTS mano_obra (
            codigo TEXT PRIMARY KEY,
            descripcion TEXT NOT NULL,
            unidad TEXT NOT NULL,
            precio REAL NOT NULL
        )
    """,
    "herramientas": """
        CREATE TABLE IF NOT EXISTS herramientas (
            codigo TEXT PRIMARY KEY,
            descripcion TEXT NOT NULL,
            unidad TEXT NOT NULL,
            precio REAL NOT NULL
        )
    """,
    "transporte": """
        CREATE TABLE IF NOT EXISTS transporte (
            codigo TEXT PRIMARY KEY,
            descripcion TEXT NOT NULL,
            unidad TEXT NOT NULL,
            precio REAL NOT NULL
        )
    """,
     "estructura": """
        CREATE TABLE IF NOT EXISTS estructura (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo_estructura TEXT NOT NULL,
            tipo_insumo TEXT NOT NULL,       -- 'material', 'mano_obra', 'herramienta', 'transporte'
            codigo_insumo TEXT NOT NULL,
            cantidad REAL NOT NULL
        )
    """
    
}
