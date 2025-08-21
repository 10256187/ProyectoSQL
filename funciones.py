# función que define la suma de un rango continuo de números
def suma_hasta(n):
    suma = 0
    for i in range (1,n+1):
        suma = suma + i
    return suma
# Función que define el factrial de un rango de numeros
def factorial_hasta(n):
    if n == 0:
        factorial = 1
        return factorial
    else:
        factorial = 1
        for i in range (1,n+1):
            factorial = factorial*i
        return factorial
def fibonacci(n):
    serie = []
    a, b = 0, 1
    for _ in range(n):
        serie.append(a)
        a, b = b, a + b
    return serie
# programa principal
n = int(input("hasta que número quiere las operacones: "))
print("La suma de los: ",n,"Primeros números es:",suma_hasta(n))
print("La serie de fibonacci de los: ",n,"pPrimeros números es:",fibonacci(n))
print("El factroial",n," es:",factorial_hasta(n))

for letra in ("José"):
    print(letra)
    
for i in range(1,n):
    if i == 5:
        continue
    print(i)
    
for i in range(1,n):
    if i >= 5:
        break
    print(i)