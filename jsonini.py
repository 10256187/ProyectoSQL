personas = []

cantidad = int(input("¿Cuántas personas deseas registrar?: "))
for i in range(cantidad):
    print(f"\nPersona {i + 1}:")
    persona = {}
    persona["nombre"] = input("Nombre: ")
    persona["edad"] = int(input("Edad: "))  # Guardamos la edad como número
    persona["ciudad"] = input("Ciudad: ")
    personas.append(persona)
    
    #Busqeda en un diccionario
nombre_buscado = input("\n¿A quién deseas buscar?: ")
encontrado = False

for p in personas:
    if p["nombre"].lower() == nombre_buscado.lower():
        print(f"{p['nombre']} tiene {p['edad']} años y vive en {p['ciudad']}")
        encontrado = True
        break
if not encontrado:
    print("Persona no encontrada.")
    
# Cálculo del promedio de edades
total_edades = 0

for p in personas:
    total_edades += p["edad"]

promedio = total_edades / len(personas)
print(f"\nEl promedio de edad es: {promedio:.2f}")

# Convertir JSON
import json

json_texto = json.dumps(personas, indent=4)
print("\nFormato JSON de los datos:")
print(json_texto)

# Abrimos un archivo en modo escritura ("w") y lo llamamos datos.json
with open("datos.json", "w", encoding="utf-8") as archivo:
    json.dump(personas, archivo, indent=4, ensure_ascii=False)

print("✅ Archivo 'datos.json' guardado correctamente.")