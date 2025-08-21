import json
import os

archivo_json = "materiales.json"


# Cargar datos desde el archivo (si existe)
def cargar_materiales():
    if os.path.exists(archivo_json):
        with open(archivo_json, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

# Función para agregar un nuevo material
def agregar_material():
    print("\n🟢 Agregar nuevo material")
    
    codigo = input("Código (ej: ccu-001): ").strip()
    descripcion = input("Descripción: ").strip()
    unidad = input("Unidad (ej: Ml, Kg, Und): ").strip()
    
    try:
        precio = float(input("Precio (ej: 2500): ").replace(",", "."))
        peso = float(input("Peso (kg o similar): ").replace(",", "."))
    except ValueError:
        print("❌ Error: el precio y el peso deben ser números.")
        return

    material = {
        "codigo": codigo,
        "descripcion": descripcion,
        "unidad": unidad,
        "precio": precio,
        "peso": peso
    }
    
    materiales.append(material)  # <-- ESTA LÍNEA FALTABA
    guardar_materiales()         # Guardar justo después de agregar
    print("✅ Material agregado con éxito.")

# Función para mostrar materiales
def ver_materiales():
    print("\n📋 Lista de materiales registrados:")
    if not materiales:
        print("⚠️ No hay materiales aún.")
        return
    
    for mat in materiales:
        print(f"- {mat['codigo']} | {mat['descripcion']} | {mat['unidad']} | ${mat['precio']} | {mat['peso']}kg")

# Guardar datos al archivo
def guardar_materiales():
    with open(archivo_json, "w", encoding="utf-8") as f:
        json.dump(materiales, f, indent=4, ensure_ascii=False)

# ===== PROGRAMA PRINCIPAL =====

materiales = cargar_materiales()  # Cargar los datos al iniciar

while True:
    print("\n===== Archivo maestro de insumos =====")
    print("1. Agregar material")
    print("2. Ver materiales")
    print("3. Salir")

    opcion = input("Elige una opción: ").strip()

    if opcion == "1":
        agregar_material()
    elif opcion == "2":
        ver_materiales()
    elif opcion == "3":
        print("💾 Guardando y saliendo... ¡Hasta luego!")
        guardar_materiales()
        break
    else:
        print("❌ Opción inválida.")
