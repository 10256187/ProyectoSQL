# validaciones.py
import sqlite3
import re

def crear_tablas_si_no_existen(nombre_base):
    try:
        with sqlite3.connect(nombre_base) as conexion:
            cursor = conexion.cursor()
            tablas = {
                "materiales": "codigo TEXT PRIMARY KEY, descripcion TEXT, unidad TEXT, precio REAL, peso REAL", 
                "mano_obra": "codigo TEXT PRIMARY KEY, descripcion TEXT, unidad TEXT, precio REAL",
                "herramientas": "codigo TEXT PRIMARY KEY, descripcion TEXT, unidad TEXT, precio REAL",
                "transporte": "codigo TEXT PRIMARY KEY, descripcion TEXT, unidad TEXT, precio REAL"
            }
            for tabla, columnas in tablas.items():
                cursor.execute(f"CREATE TABLE IF NOT EXISTS {tabla} ({columnas})")
    except Exception as e:
        print(f"❌ Error creando las tablas: {e}")


def leer_codigo(prompt="Ingrese el código (AAAA_1234): ", permitir_vacio=False):
    while True:
        codigo = input(prompt).strip().upper()
        if not codigo and permitir_vacio:
            return ""
        
        # Insertar guion si falta y el patrón es válido
        if re.fullmatch(r"[A-Z]{4}[0-9]{4}", codigo):
            codigo = codigo[:4] + "-" + codigo[4:]

        if re.fullmatch(r"[A-Z]{4}-[0-9]{4}", codigo):
            return codigo
        else:
            print("❌ Código inválido. Formato esperado: 4 letras, guion bajo, 4 números (ej: ABCD_1234).")

def leer_descripcion(prompt="Ingrese la descripción: ", permitir_vacio=False):
    while True:
        descripcion = input(prompt).strip()
        if descripcion or permitir_vacio:
            return descripcion
        print("❌ La descripción no puede estar vacía.")

def leer_valor_numerico(prompt="Ingrese un valor numérico: ", permitir_vacio=False):
    while True:
        valor = input(prompt).strip().replace(",", ".")
        if not valor and permitir_vacio:
            return ""
        try:
            numero = float(valor)
            if numero >= 0:
                return numero
            else:
                print("❌ El valor no puede ser negativo.")
        except ValueError:
            print("❌ Por favor, ingrese un número válido.")

def leer_unidad(tipo="material", prompt="Ingrese la unidad: ", permitir_vacio=False):
    unidades_por_tipo = {
        "material":    ["ML", "M³", "M²", "KM", "LB", "KG", "LT", "CM", "GL", "GB", "HZ", "UN", "SC", "CT", "PT", "CÑ"],
        "mano_obra":   ["HH", "DD", "JN", "MS", "HN"],
        "herramienta": ["DD", "MS", "HR", "UN"],
        "transporte":  ["TK", "VJ", "M³", "MS", "DD", "HR", "VK"],
        "estructura":  ["ML", "M³", "M²", "KM", "PG", "KG", "GB", "UN", "VJ"]
    }

    unidades_validas = unidades_por_tipo.get(tipo.lower(), [])

    while True:
        unidad = input(prompt).strip().upper()
        if not unidad and permitir_vacio:
            return ""
        if unidad in unidades_validas:
            return unidad
        else:
            print(f"❌ Unidad inválida para tipo '{tipo}'. Opciones válidas: {', '.join(unidades_validas)}")

# ✅ Alias para mejorar la legibilidad del código en distintos contextos
leer_precio = leer_valor_numerico
leer_peso = leer_valor_numerico
leer_valor_mano_obra = leer_valor_numerico
leer_valor_herramienta = leer_valor_numerico
leer_valor_transporte = leer_valor_numerico
