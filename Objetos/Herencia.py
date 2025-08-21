class Animal:
    def __init__(self, nombre, edad):
        self.__nombre = nombre    # atributo privado
        self.__edad = edad        # atributo privado

    # Getter y setter para nombre
    def get_nombre(self):
        return self.__nombre

    def set_nombre(self, nuevo_nombre):
        self.__nombre = nuevo_nombre

    # Getter y setter para edad
    def get_edad(self):
        return self.__edad

    def set_edad(self, nueva_edad):
        self.__edad = nueva_edad

    def presentarse(self):
        print(f"Hola, soy {self.__nombre} y tengo {self.__edad} años.")

# Clase hija de animal
class Perro(Animal):
    def __init__(self, nombre, edad, raza, sonido):
        super().__init__(nombre, edad)
        self.__raza = raza        # privado
        self.__sonido = sonido    # privado

    def hacer_sonido(self):
        print(f"{self.get_nombre()} dice: {self.__sonido}")

    def mostrar_raza(self):
        print(f"{self.get_nombre()} es un {self.__raza}")
        
#Clase hija de animal para mostrar la herencia
class Gato(Animal):
    def __init__(self, nombre, edad, color):
        super().__init__(nombre, edad)
        self.__color = color  # privado

    def maullar(self):
        print(f"{self.get_nombre()} dice: MIAU 🐱")

    def mostrar_color(self):
        print(f"{self.get_nombre()} es de color {self.__color}")
#miremos como funciona lo de la herencia
# Creamos objetos
brandy = Perro("Brandy", 8, "Cocker", "GUAAAU!")
luna = Gato("Luna", 3, "blanco")

# Usamos métodos de Animal (heredados)
brandy.presentarse()
brandy.hacer_sonido()
brandy.mostrar_raza()

print("----")

luna.presentarse()
luna.maullar()
luna.mostrar_color()

# Cambiamos el nombre usando set
luna.set_nombre("Mish")
luna.presentarse()