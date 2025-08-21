# logica_db.py
import mysql.connector
from mysql.connector import Error
from tkinter import messagebox

# Función de conexión a la base de datos
def conectar_db():
    """
    Establece la conexión a la base de datos MySQL.
    """
    try:
        conn = mysql.connector.connect(
            host='localhost', 
            user='root', 
            password='123@Chepe$#', 
            database='ProyectoSQL'
        )
        if conn.is_connected():
            return conn
    except Error as e:
        messagebox.showerror("Error de Conexión", f"Error al conectar con la base de datos MySQL: {e}")
        return None

def buscar_componente_en_db(codigo):
    """
    Busca un componente en todas las tablas de la base de datos (materiales, mobra, etc.).
    Retorna una tupla (descripcion, unidad, precio, tipo) o None si no se encuentra.
    """
    conn = conectar_db()
    if conn is None:
        return None
        
    try:
        cursor = conn.cursor()
        
        # Tablas a buscar y sus prefijos correspondientes para saber de qué tipo es el componente
        tablas = {
            'materiales': 'Materiales',
            'mobra': 'Mano de Obra',
            'herramienta': 'Herramienta y Equipo',
            'transporte': 'Transporte'
        }
        
        for tabla, tipo in tablas.items():
            cursor.execute(f"SELECT descripcion, unidad, precio FROM {tabla} WHERE codigo = %s", (codigo,))
            resultado = cursor.fetchone()
            if resultado:
                # Retorna la descripción, unidad, precio y el tipo de componente
                return resultado + (tipo,) 
        
        return None
    except Error as e:
        messagebox.showerror("Error de Búsqueda", f"Error al buscar el componente: {e}")
        return None
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def insertar_analisis_unitario(codigo_analisis, componentes):
    """
    Guarda todos los componentes de un análisis unitario en la tabla 'analisis_unitarios'.
    Si el código de análisis ya existe, elimina los registros anteriores y los reemplaza.
    
    :param codigo_analisis: El código del análisis unitario principal (ej. 'CONC-2500').
    :param componentes: Una lista de diccionarios, donde cada diccionario contiene la información
                        de un componente (código, descripción, cantidad, precio, etc.).
    """
    conn = conectar_db()
    if conn is None:
        return False
        
    try:
        cursor = conn.cursor()
        
        # Eliminar registros anteriores para el mismo código de análisis.
        # Esto previene duplicados al editar un análisis.
        cursor.execute("DELETE FROM analisis_unitarios WHERE codigo_analisis = %s", (codigo_analisis,))
        
        # Insertar los nuevos componentes
        for comp in componentes:
            cursor.execute("""
                INSERT INTO analisis_unitarios (
                    codigo_analisis, tipo_componente, codigo_componente, descripcion, 
                    unidad, cantidad, precio, valor_parcial
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                codigo_analisis, 
                comp['tipo'], 
                comp['codigo'], 
                comp['descripcion'], 
                comp['unidad'], 
                comp['cantidad'], 
                comp['precio'], 
                comp['valor_parcial']
            ))
        
        conn.commit()
        return True
    except Error as e:
        messagebox.showerror("Error de Inserción", f"Error al guardar el análisis unitario: {e}")
        return False
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def obtener_analisis_unitario(codigo_analisis):
    """
    Obtiene todos los componentes de un análisis unitario dado su código.
    
    :param codigo_analisis: El código del análisis unitario a buscar.
    :return: Una lista de diccionarios con la información de los componentes,
             o una lista vacía si no se encuentra.
    """
    conn = conectar_db()
    if conn is None:
        return []
        
    try:
        cursor = conn.cursor(dictionary=True) # Retorna los resultados como diccionarios
        cursor.execute("""
            SELECT codigo_analisis, tipo_componente, codigo_componente, descripcion, unidad, cantidad, precio, valor_parcial 
            FROM analisis_unitarios WHERE codigo_analisis = %s
        """, (codigo_analisis,))
        
        resultados = cursor.fetchall()
        return resultados
    except Error as e:
        messagebox.showerror("Error de Lectura", f"Error al obtener los datos del análisis: {e}")
        return []
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
