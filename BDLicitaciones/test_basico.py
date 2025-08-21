# test_basico.py

from gestores import GestorMaterialesSQLite
from validaciones import leer_codigo, leer_descripcion, leer_unidad, leer_valor_unitario
import os

gestor = GestorMaterialesSQLite("materiales.db")

print("🔎 Buscar o agregar material")
codigo = leer_codigo("Ingrese código de material: ", gestor._existe_codigo)

# Buscar en base de datos
material = gestor.buscar_material(codigo)

if material:
    print("\n📦 Material encontrado:")
    print(f"- Código: {material[0]}")
    print(f"- Descripción: {material[1]}")
    print(f"- Unidad: {material[2]}")
    print(f"- Precio: ${material[3]:,.2f}")
    print(f"- Peso: {material[4]} kg")
else:
    print("❌ Material no encontrado. Vamos a agregarlo.")
    descripcion = leer_descripcion()
    unidad = leer_unidad()
    valor_unitario = leer_valor_unitario()
    peso = float(input("Ingrese peso por unidad en kg: "))

    # Crear objeto y guardar
    from modelos import Material
    nuevo_material = Material(codigo, descripcion, unidad, valor_unitario, peso)
    gestor._guardar_material(nuevo_material)

    print("✅ Material agregado con éxito.")