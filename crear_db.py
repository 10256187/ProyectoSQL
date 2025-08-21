<<<<<<< HEAD
import sqlite3

# Conectar a la base de datos (o crearla si no existe)
conn = sqlite3.connect('bddatos.db')
cursor = conn.cursor()

# Insertar un nuevo material
sql_insert = "INSERT INTO materiales (codigo, descripcion, unidad, precio, peso, tipo) VALUES (1, 'Tornillo', 'unidad', 0.50, 0.01, 'Metalico');"
cursor.execute(sql_insert)

conn.commit()

conn.close()
=======
# -*- coding: utf-8 -*-
"""
Módulo con funciones genéricas para realizar operaciones de CRUD (Crear, Leer,
Actualizar y Eliminar) en la base de datos.
"""
import mysql.connector
from mysql.connector import Error
from tkinter import messagebox
import re

# Constantes de la base de datos
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '123@Chepe$#', # Se ha añadido la contraseña aquí
    'database': 'ProyectoSQL'
}

# --- Funciones de Conexión y Validaciones Básicas ---

def conectar_bd():
    """Conecta a la base de datos y retorna el objeto de conexión."""
    try:
        mydb = mysql.connector.connect(**DB_CONFIG)
        return mydb
    except Error as err:
        messagebox.showerror(
            "Error de Conexión",
            f"❌ Error al conectar a la base de datos: {err}\n\nAsegúrate de que el servidor MySQL esté corriendo."
        )
        return None

def validar_codigo(codigo_str):
    """Valida el formato de código AAAA-1234."""
    codigo = codigo_str.strip().upper()
    if re.fullmatch(r"^[A-Z]{4}[0-9]{4}$", codigo):
        codigo = codigo[:4] + "-" + codigo[4:]
    
    if re.fullmatch(r"^[A-Z]{4}-[0-9]{4}$", codigo):
        return codigo
    else:
        messagebox.showerror(
            "Error de Validación",
            "❌ El código no cumple con el formato AAAA-1234. Por favor, corrígelo."
        )
        return None

def validar_valor_numerico(valor_str):
    """Valida que un valor sea un número no negativo."""
    if not valor_str.strip():
        return None
    try:
        numero = float(valor_str.strip().replace(",", "."))
        if numero >= 0:
            return numero
        else:
            messagebox.showerror("Error de Validación", "❌ El valor no puede ser negativo.")
            return None
    except ValueError:
        messagebox.showerror("Error de Validación", "❌ Por favor, ingrese un número válido.")
        return None

# --- Funciones Genéricas para la Base de Datos ---

def insertar_registro(table_name, entry_fields, window):
    """Inserta un registro genérico en la BD."""
    mydb = conectar_bd()
    if not mydb: return
    cursor = mydb.cursor()

    try:
        # Extraer y validar datos
        data = {key: entry.get() for key, entry in entry_fields.items()}
        data['codigo'] = validar_codigo(data['codigo'])
        data['precio'] = validar_valor_numerico(data['precio'])
        
        if table_name == 'materiales':
            data['peso'] = validar_valor_numerico(data['peso'])
        
        if not all(data.values()): # Validamos que no haya datos None después de la validación
            return

        campos = ', '.join(data.keys())
        placeholders = ', '.join(['%s'] * len(data))
        sql = f"INSERT INTO {table_name} ({campos}) VALUES ({placeholders})"
        val = tuple(data.values())

        cursor.execute(sql, val)
        mydb.commit()
        messagebox.showinfo("Éxito", f"✅ Registro insertado en la tabla '{table_name}' con éxito!")
        window.destroy()

    except Error as err:
        messagebox.showerror("Error de Inserción", f"❌ Error al insertar en la tabla '{table_name}': {err}")
    finally:
        if cursor: cursor.close()
        if mydb and mydb.is_connected(): mydb.close()

def obtener_registros(table_name):
    """Obtiene todos los registros de una tabla genérica."""
    mydb = conectar_bd()
    if not mydb: return []
    cursor = mydb.cursor()
    try:
        cursor.execute(f"SELECT * FROM {table_name}")
        return cursor.fetchall()
    except Error as err:
        messagebox.showerror("Error al obtener datos", f"❌ Error al obtener datos de la tabla '{table_name}': {err}")
        return []
    finally:
        if cursor: cursor.close()
        if mydb and mydb.is_connected(): mydb.close()
        
def actualizar_registro(table_name, entry_fields, window, codigo_original, treeview):
    """Actualiza un registro genérico en la BD."""
    mydb = conectar_bd()
    if not mydb: return
    cursor = mydb.cursor()

    try:
        # Extraer y validar datos
        data = {key: entry.get() for key, entry in entry_fields.items()}
        data['precio'] = validar_valor_numerico(data['precio'])
        
        if table_name == 'materiales':
            data['peso'] = validar_valor_numerico(data['peso'])
        
        if not all(data.values()):
            return
            
        sets = ', '.join([f"{key} = %s" for key in data.keys()])
        sql = f"UPDATE {table_name} SET {sets} WHERE codigo = %s"
        val = tuple(data.values()) + (codigo_original,)
        
        cursor.execute(sql, val)
        mydb.commit()
        messagebox.showinfo("Éxito", f"✅ Registro '{codigo_original}' en la tabla '{table_name}' actualizado con éxito!")
        
        # Recargar Treeview
        for item in treeview.get_children():
            treeview.delete(item)
        datos_actualizados = obtener_registros(table_name)
        for row in datos_actualizados:
            treeview.insert('', 'end', values=row)

        window.destroy()
    except Error as err:
        messagebox.showerror("Error de Actualización", f"❌ Error al actualizar registro en la tabla '{table_name}': {err}")
    finally:
        if cursor: cursor.close()
        if mydb and mydb.is_connected(): mydb.close()
>>>>>>> 6b069589aa7a2efcb39fa2a7e4de5280ce0ddfce
