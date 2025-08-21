#iniciando con manejo de archivos

#Escribir en un archivo
archivo = open("saludo.txt", "w")
archivo.write("Hola, Chepe ")
archivo.write("Bienvenido al mundo de los archivos en Python\n")
archivo.close()

#Leer un archivo
archivo = open("saludo.txt", "r")
contenido = archivo.read()
print(contenido)
archivo.close()

archivo = open("saludo.txt", "w")
archivo.write("Hola, Chepe ")
archivo.write("Bienvenido al mundo de los archivos en Python\n")
archivo.close()

nombre = input("¿Cómo te llamas?: ")
edad = input("¿Qué edad tienes?: ")
#Creamos el archivo en modo escritura
archivo = open("usuario.txt", "w")
#Guardamos información en el archivo
archivo.write(f"Nombre: {nombre}\n")
archivo.write(f"Edad: {edad}\n")
# Cerramos el archivo
archivo.close()

#Ahora lo abrimos para leer
archivo = open("usuario.txt", "r")

#Leemos todo el contenido
contenido = archivo.read()

#Mostramos el contenido en la pantalla
print("\nContenido del archivo:")
print(contenido)

#cerramos el archivo (¡siempre hay que hacerlo!)
archivo.close()