import json
import os
import re

archivo_json = "materiales.json"

def cargar_materiales():
    if os.path.exists(archivo_json):
        with open(archivo_json, "r", encoding="utf-8") as f:
            datos = json.load(f)
            datos.sort(key=lambda x: x["codigo"].lower())  # Ordena al cargar
            return datos
    return []

def guardar_materiales(materiales):
    with open(archivo_json, "w", encoding="utf-8") as f:
        json.dump(materiales, f, indent=4, ensure_ascii=False)

def agregar_material(materiales):
    print("\n🟢 Agregar nuevo material")
    
    while True:
        cod = input("Código (formato: AAAANNNN o AAAA-NNNN): ").strip().upper()

        # Inserta "-" si no lo escriben
        if re.match(r"^[A-Z]{4}\d{4}$", cod):
            cod = cod[:4] + "-" + cod[4:]

        if not re.match(r"^[A-Z]{4}-\d{4}$", cod):
            print("❌ Código inválido. Usa 4 letras, guion, 4 números (ej: ABCD-1234).")
            continue

        if any(mat["codigo"] == cod for mat in materiales):
            print("⚠️ Ya existe un material con ese código.")
            continue
        codigo = cod
        break
    descripcion = input("Descripción: ").strip()
    
    unidades_validas = ["Ml", "Kg", "Lt", "cm", "mL", "gL", "Hz", "Un", "Sc", "m³","m²","pg", "pt", "cñ"]
    while True:
        unidad = input("Unidad (ej: Ml, Un, M³): ").strip()

        # Validación con expresión regular:
        if not re.match(r"^[A-Za-z][A-Za-z0-9]$", unidad):
            print("❌ Unidad inválida. Debe tener 2 caracteres: el primero una letra, el segundo letra o número.")
            continue

        break
    
    try:
        precio = float(input("Precio (ej: 2500): ").replace(",", "."))
        peso = float(input("Peso (por unidad de medida): ").replace(",", "."))
    except ValueError:
        print("❌ Error: el precio y el peso deben ser números.")
        return

    # Verificamos si el código ya existe
    if any(mat["codigo"] == codigo for mat in materiales):
        print("⚠️ Ya existe un material con ese código.")
        return

    material = {
        "codigo": codigo,
        "descripcion": descripcion,
        "unidad": unidad,
        "precio": precio,
        "peso": peso
    }

    materiales.append(material)
    materiales.sort(key=lambda x: x["codigo"].lower())  # 🔀 Ordena por código
    guardar_materiales(materiales)
    print("✅ Material agregado con éxito.")

def ver_materiales(materiales):
    print("\n📋 Lista de materiales registrados:")
    if not materiales:
        print("⚠️ No hay materiales aún.")
        return
    
    for mat in materiales:
        print(f"- {mat['codigo']} | {mat['descripcion']} | {mat['unidad']} | ${mat['precio']} | {mat['peso']}kg")
        

# Editar material
def editar_material(materiales):
    print("\n✏️ Editar material")

    if not materiales:
        print("⚠️ No hay materiales para editar.")
        return

    cod_buscar = input("Ingresa el código del material a editar: ").strip().upper()
    if re.match(r"^[A-Z]{4}\d{4}$", cod_buscar):
        cod_buscar = cod_buscar[:4] + "-" + cod_buscar[4:]

    for mat in materiales:
        if mat["codigo"] == cod_buscar:
            print(f"\n🔍 Editando {mat['codigo']} - {mat['descripcion']}")

            nuevo_codigo = input(f"Código nuevo [{mat['codigo']}]: ").strip().upper()
            if nuevo_codigo:
                if re.match(r"^[A-Z]{4}\d{4}$", nuevo_codigo):
                    nuevo_codigo = nuevo_codigo[:3] + "-" + nuevo_codigo[3:]
                if not re.match(r"^[A-Z]{4}-\d{4}$", nuevo_codigo):
                    print("❌ Código inválido. Se mantiene el anterior.")
                elif any(m["codigo"] == nuevo_codigo and m != mat for m in materiales):
                    print("⚠️ Ese código ya está en uso. Se mantiene el anterior.")
                else:
                    mat["codigo"] = nuevo_codigo

            nueva_desc = input(f"Descripción nueva [{mat['descripcion']}]: ").strip()
            if nueva_desc:
                mat["descripcion"] = nueva_desc

            nueva_unidad = input(f"Unidad nueva [{mat['unidad']}]: ").strip().upper()
            if nueva_unidad:
                if re.match(r"^[A-Z][A-Z0-9]$", nueva_unidad):
                    mat["unidad"] = nueva_unidad
                else:
                    print("❌ Unidad inválida. Se mantiene la anterior.")

            nuevo_precio = input(f"Precio nuevo [{mat['precio']}]: ").replace(",", ".").strip()
            if nuevo_precio:
                try:
                    mat["precio"] = float(nuevo_precio)
                except ValueError:
                    print("❌ Precio inválido. Se mantiene el anterior.")

            nuevo_peso = input(f"Peso nuevo [{mat['peso']}]: ").replace(",", ".").strip()
            if nuevo_peso:
                try:
                    mat["peso"] = float(nuevo_peso)
                except ValueError:
                    print("❌ Peso inválido. Se mantiene el anterior.")

            materiales.sort(key=lambda x: x["codigo"])
            print("✅ Material actualizado y reordenado por código.")
            return

    print("❌ Código no encontrado.")