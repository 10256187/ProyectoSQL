# lista ---> se puede modificar
frutas = ["manzana", "banana", "naranja"]
for fruta in frutas:
    print("Me gusta la", fruta)
frutas.append("mandarina")
for fruta in frutas:
    print("Me gusta la", fruta)
    
# Tuplas ---> No pueden ser modificadas
dias = ("lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo")
print("Los dás de la semana son:")
for dia in dias:
    print(dia)
    
# Diccionarios inicio
# Paso 1: Creamos un diccionario vacío
persona = {}

# Paso 2: Pedimos datos al usuario
persona["nombre"] = input("¿Cuál es tu nombre: ")
persona["edad"] =   input("¿Qué edad tienes  : ")
persona["ciudad"] = input("¿Dónde vives      : ")

# Paso 3: Mostramos los datos usando un ciclo
print("\n--- Datos de la persona ---")
for clave, valor in persona.items():
    print(f"{clave.capitalize()}: {valor}")