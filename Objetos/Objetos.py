# perro.py

class Perro:
    def __init__(self, nombre, raza, edad, sonido):
        self.__nombre = nombre   # ahora es "privado"
        self.__raza = raza
        self.__edad = edad
        self.__sonido = sonido

    # 👉 Getter: para leer el nombre
    def get_nombre(self):
        return self.__nombre

    # 👉 Setter: para cambiar el nombre
    def set_nombre(self, nuevo_nombre):
        if nuevo_nombre:  # validación sencilla
            self.__nombre = nuevo_nombre

    def presentarse(self):
        print(f"🐾 Hola, soy {self.__nombre}, un {self.__raza} de {self.__edad}.")

    def hacer_sonido(self):
        print(f"{self.__nombre} dice: {self.__sonido}")