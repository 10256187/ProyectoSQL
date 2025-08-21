# entrada_consola.py
from logica import agregar_material

def agregar_material_consola():
    data = {
        "codigo": input("Código: "),
        "descripcion": input("Descripción: "),
        "unidad": input("Unidad: "),
        "precio": input("Precio: ")
    }
    if agregar_material(data):
        print("✅ Material agregado correctamente.")