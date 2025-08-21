# validaciones.py

import re

# ✅ Validar código con opción de permitir vacío (para edición)
def leer_codigo(prompt, existe_codigo_func=None, permitir_vacio=False):
    while True:
        codigo = input(prompt).strip().upper()

        if not codigo and permitir_vacio:
            return ""

        if re.match(r"^[A-Z]{4}\d{4}$", codigo):
            codigo = codigo[:4] + "-" + codigo[4:]

        if re.match(r"^[A-Z]{4}-\d{4}$", codigo):
            if existe_codigo_func and existe_codigo_func(codigo):
                print("❌ El código ya existe. Intente con otro.")
            else:
                return codigo
        else:
            print("❌ Código inválido. Debe tener el formato AAAA-NNNN.")


# ✅ Validar descripción

def leer_descripcion(prompt="Descripción: ", permitir_vacio=False):
    while True:
        descripcion = input(prompt).strip()
        if descripcion or permitir_vacio:
            return descripcion
        print("❌ La descripción no puede estar vacía.")


# ✅ Validar unidad según lista válida

def leer_unidad(unidades_validas, prompt="Unidad: ", permitir_vacio=False):
    while True:
        unidad = input(prompt).strip().upper()
        if not unidad and permitir_vacio:
            return ""
        if unidad in unidades_validas:
            return unidad
        print("❌ Unidad inválida. Usa una de estas:", ", ".join(unidades_validas))


# ✅ Validar valor unitario (float)

def leer_valor_unitario(prompt="Precio: ", permitir_vacio=False):
    while True:
        entrada = input(prompt).strip().replace(",", ".")
        if not entrada and permitir_vacio:
            return ""
        try:
            valor = float(entrada)
            return valor
        except ValueError:
            print("❌ Valor inválido. Ingrese un número válido.")
