# Lista vacía para almacenar personas
personas = []

# ¿Cuántas personas vamos a ingresar?
cantidad = int(input("¿Cuántas personas deseas registrar?: "))
# Repetimos según la cantidad ingresada
for i in range(cantidad):
    print(f"\nPersona {i + 1}:")
    persona = {}  # Diccionario para una persona
    
    persona["nombre"] = input("Nombre: ")
    persona["edad"] = input("Edad: ")
    persona["ciudad"] = input("Ciudad: ")
# Agregamos el diccionario a la lista
    personas.append(persona)
# Mostramos todos los datos al final
print("\n=== Lista de Personas Registradas ===")
for p in personas:
    print(f"{p['nombre']} tiene {p['edad']} años y vive en {p['ciudad']}")