# Inicio de set {}
frutas = {"manzana", "banana", "naranja", "banana"}
print(frutas)
frutas.add("pera")
print(frutas)

a = {1, 2, 3}
b = {3, 4, 5}

print(a.union(b))        # {1, 2, 3, 4, 5}
print(a.intersection(b)) # {3}
print(a.difference(b))   # {1, 2}
print(b.difference(a))   # {4, 5}

#Ejemplo práctico de set, Conjunto total de estudiantes

todos_los_estudiantes = {
    "Ana", "Luis", "Carlos", "Diana", "Beatriz", "Mateo", "Sara"
}

# Estudiantes inscritos en Matemáticas
matematicas = {"Ana", "Luis", "Carlos", "Beatriz"}

# Estudiantes inscritos en Física
fisica = {"Carlos", "Diana", "Mateo"}

# Unión - Están en al menos una materia
al_menos_una = matematicas | fisica
print("Estudiantes en al menos una materia:", al_menos_una)

# Intersección - Están en ambas
en_ambas = matematicas & fisica
print("Estudiantes en ambas materias:", en_ambas)

# Diferencia - Solo en Matemáticas
solo_mate = matematicas - fisica
print("Estudiantes solo en Matemáticas:", solo_mate)

# Diferencia simétrica - En una sola
una_sola = matematicas ^ fisica
print("Estudiantes en solo una materia:", una_sola)

# Complemento simulado - Están en el total pero no en Física
no_en_fisica = todos_los_estudiantes - fisica
print("Estudiantes que no están en Física:", no_en_fisica)

# El otro ejemplo de set
# Conjuto total de estudiantes
todos = {
    "Laura", "Andrés", "Camila", "Esteban", "Natalia", "Carlos", "Valeria", "Tomás", "Daniela"
}
#Estudiantes en pintura
pintura = {
    "Laura", "Andrés", "Camila", "Esteban", "Natalia"
}
#Estudaintes en tenis
tenis = {
    "Esteban", "Carlos", "Camila", "Valeria", "Laura"
}
# Estudiantes en ambas actividades
en_pintura_y_tenis = pintura & tenis
print("Los que estan en pintura y tenis son:", en_pintura_y_tenis)
# Estudiantes en una de las dos actividades
en_una_de_Las_dos = pintura | tenis
print("Los que estan en tenis o pintura:", en_una_de_Las_dos)
# Estudiantes en solo pintura
solo_pintura = pintura ^ tenis
print("Los que estan solo pintura:", solo_pintura)
# Estudiantes en una al menos una de las dos actividades
al_menos_una = pintura - tenis
print("Los que estan por lo menos en una:", al_menos_una)
# Estudiantes que no participaron en ninguna actividad
ninguna_actividad =  en_pintura_y_tenis - todos
print("No participaron en ninguna actividad:", ninguna_actividad)