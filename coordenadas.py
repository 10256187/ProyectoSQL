import turtle
import numpy as np

# Configuració de  pantalla
pantalla = turtle.Screen()
pantalla.title("Tablero de coordenadas con Turtle")
pantalla.setup(width=800, height=600)
pantalla.bgcolor("white")

# Crear tortuga para dibujar los ejes
ejes = turtle.Turtle()
ejes.speed(0)
ejes.pensize(2)
ejes.color("black")

# Dibujar eje X
ejes.penup()
ejes.goto(-390, 0)  # desde la izquierda
ejes.pendown()
ejes.goto(390, 0)   # hasta la derecha

# Dibujar eje Y
ejes.penup()
ejes.goto(0, -290)  # desde abajo
ejes.pendown()
ejes.goto(0, 290)   # hasta arriba

# Crear tortuga para marcar coordenadas
marcas = turtle.Turtle()
marcas.speed(0)
marcas.hideturtle()
marcas.penup()

# Marcar coordenadas en X cada 100 píxeles
for x in np.arange(-1.0, 1.1, 0.1):
    if round(x, 2) != 0:
        marcas.goto(x * 100, -10)  # Escalamos x
        marcas.write(str(round(x, 1)), align="center", font=("Arial", 8, "normal"))

# Marcar coordenadas en Y cada 100 píxeles
for y in range(-200, 201, 100):
    if y != 0:
        marcas.goto(10, y - 5)
        marcas.write(str(y), align="left", font=("Arial", 6, "normal"))
# programa principal
pantalla.exitonclick()