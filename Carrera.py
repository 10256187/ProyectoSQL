import turtle
import random
import time

# Configurar la pantalla
pantalla = turtle.Screen()
pantalla.title("Carrera de la Tortuga y el Conejo 🐢🐇")
pantalla.bgcolor("lightgreen")

# Crear la tortuga
tortuga = turtle.Turtle()
tortuga.color("green")
tortuga.shape("turtle")
tortuga.penup()
tortuga.goto(-300, 20)
tortuga.pendown()

# Crear el conejo
conejo = turtle.Turtle()
conejo.color("gray")
conejo.shape("turtle")
conejo.penup()
conejo.goto(-300, -20)
conejo.pendown()

# Dibujar la meta
meta = 350
meta_linea = turtle.Turtle()
meta_linea.penup()
meta_linea.goto(meta, 50)
meta_linea.pendown()
meta_linea.right(90)
meta_linea.forward(100)
meta_linea.hideturtle()

# Carrera
print("posición de la tortuga:",tortuga.xcor())
print("posición del Conejo   :",conejo.xcor())
while (tortuga.xcor() < 350) and conejo.xcor() < 350:
    tortuga.forward(random.randint(1, 100))
    conejo.forward(random.randint(1, 100))
    time.sleep(0.1)

# Ganador
ganador = turtle.Turtle()
ganador.hideturtle()
ganador.penup()
ganador.goto(0, 150)

if tortuga.xcor() >= 350 and conejo.xcor() >= 350:
    ganador.write("¡Empate!", align="center", font=("Arial", 20, "bold"))
elif tortuga.xcor() >= 350:
    ganador.write("¡La Tortuga gana!", align="center", font=("Arial", 20, "bold"))
else:
    ganador.write("¡El Conejo gana!", align="center", font=("Arial", 20, "bold"))

#Programa principal
pantalla.mainloop()