nombre = input("como te llamas:  ")
edad = 0
# uso de while
while edad <= 0:
    edad = int(input("Que edad tienes:"))
    
    if edad <= 0:
        print(f"Hola, {nombre}. Entraste un valor invalido")
    elif edad > 62:
        print(f"Hola, {nombre}. Eres adulto mayor tienes {edad} años")
    elif (edad > 18) and (edad < 62):
        print(f"Hola, {nombre}. Eres adulto tienes {edad} años puedes estar trabajando o estudiando")
    elif (edad < 18) and (edad > 12):
        print(f"Hola, {nombre}. Eres adolecente tienes {edad} años y debes estar en el colegio")
    elif (edad < 11) and (edad > 6):
        print(f"Hola, {nombre}. Eres un niño tienes {edad} años y debes estar en primaria")
    elif (edad < 6) and (edad > 3):
        print(f"Hola, {nombre}. Eres un inberbe tienes {edad} años y debes estar en preescolar")
    elif (edad < 3) :
        print(f"Hola, {nombre}. Eres un bebe tienes {edad} años y debes estar en casa")
#uso de for iniciando uso de modo sencillo
limite = int(input("hasta que número quiere las operacones: "))
suma = 0
for i in range (1,limite):
    suma = suma + i
    print("Número: ",i)
print("La suma de los: ",i,"Primeros números es:",suma)   
