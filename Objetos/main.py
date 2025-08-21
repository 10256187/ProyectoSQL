# main.py

from Objetos import Perro

jauria = [
    Perro("Brandy", "Cocker", "8 años", "GRRRR..."),
    Perro("Nala", "Shsanda", "1 año", "WOOF!"),
]

# 🧪 Usamos getters y setters
print("Antes del cambio:")
jauria[0].presentarse()

# Cambiamos el nombre con setter
jauria[0].set_nombre("Brandon")

print("Después del cambio:")
jauria[0].presentarse()