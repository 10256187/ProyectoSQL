# Primera idea de programa en Python

from datetime import datetime
import csv

# Paso 1: Registrar un solo empleado
def registrar_empleado():
    print("\n--- Ingreso de datos del empleado ---")
    
    nombre = input("Nombre: ").strip()
    edad = int(input("Edad: "))

    while True:
        try:
            fecha_ingreso = datetime.strptime(input("Fecha de ingreso (AAAA-MM-DD): "), "%Y-%m-%d")
            fecha_salida = datetime.strptime(input("Fecha de salida (AAAA-MM-DD): "), "%Y-%m-%d")
            if fecha_salida < fecha_ingreso:
                print("⚠️ La fecha de salida no puede ser anterior a la de ingreso. Intenta de nuevo.")
                continue
            break
        except ValueError:
            print("❌ Formato inválido. Usa el formato correcto: AAAA-MM-DD")

    while True:
        try:
            salario = float(input("Salario mensual: "))
            if salario <= 0:
                print("⚠️ El salario debe ser mayor que cero.")
                continue
            break
        except ValueError:
            print("❌ Ingresa un número válido para el salario.")

    return {
        'nombre': nombre,
        'edad': edad,
        'fecha_ingreso': fecha_ingreso,
        'fecha_salida': fecha_salida,
        'salario': salario
    }

# Paso 2: Calcular liquidación
def calcular_liquidacion(salario, dias_trabajados):
    cesantias = salario * dias_trabajados / 360
    intereses = cesantias * 0.12
    prima = salario * dias_trabajados / 360
    vacaciones = salario * dias_trabajados / 720
    return {
        'cesantias': cesantias,
        'intereses': intereses,
        'prima': prima,
        'vacaciones': vacaciones
    }

# Paso 3: Guardar en archivo TXT
def guardar_en_archivo_txt(lista_empleados, archivo='personal.txt'):
    with open(archivo, 'a', encoding='utf-8') as f:
        for i, emp in enumerate(lista_empleados, 1):
            f.write(f"Empleado #{i}\n")
            f.write(f"Nombre: {emp['nombre']}\n")
            f.write(f"Edad: {emp['edad']}\n")
            f.write(f"Ingreso: {emp['fecha_ingreso'].strftime('%Y-%m-%d')}\n")
            f.write(f"Salida: {emp['fecha_salida'].strftime('%Y-%m-%d')}\n")
            f.write(f"Días trabajados: {emp['dias_trabajados']}\n")
            f.write(f"Salario: ${emp['salario']:,.2f}\n")
            f.write(f"  Cesantías: ${emp['liquidacion']['cesantias']:,.2f}\n")
            f.write(f"  Intereses: ${emp['liquidacion']['intereses']:,.2f}\n")
            f.write(f"  Prima:     ${emp['liquidacion']['prima']:,.2f}\n")
            f.write(f"  Vacaciones:${emp['liquidacion']['vacaciones']:,.2f}\n")
            f.write("-" * 50 + "\n")

# Paso 4: Leer archivo TXT
def leer_archivo_txt(archivo='personal.txt'):
    print("\n📂 Contenido del archivo:")
    try:
        with open(archivo, 'r', encoding='utf-8') as f:
            contenido = f.read()
            if contenido.strip() == "":
                print("⚠️ El archivo está vacío.")
            else:
                print(contenido)
    except FileNotFoundError:
        print("❌ El archivo no existe aún. Ingresa al menos un empleado para crearlo.")

# Paso 5: Guardar en archivo CSV (Excel)
def guardar_en_archivo_csv(lista_empleados, archivo='personal.csv'):
    with open(archivo, 'w', newline='', encoding='utf-8') as csvfile:
        campos = ['Nombre', 'Edad', 'Ingreso', 'Salida', 'Días trabajados', 'Salario',
                  'Cesantías', 'Intereses', 'Prima', 'Vacaciones']
        writer = csv.DictWriter(csvfile, fieldnames=campos)
        writer.writeheader()

        for emp in lista_empleados:
            writer.writerow({
                'Nombre': emp['nombre'],
                'Edad': emp['edad'],
                'Ingreso': emp['fecha_ingreso'].strftime('%Y-%m-%d'),
                'Salida': emp['fecha_salida'].strftime('%Y-%m-%d'),
                'Días trabajados': emp['dias_trabajados'],
                'Salario': emp['salario'],
                'Cesantías': emp['liquidacion']['cesantias'],
                'Intereses': emp['liquidacion']['intereses'],
                'Prima': emp['liquidacion']['prima'],
                'Vacaciones': emp['liquidacion']['vacaciones']
            })

# Paso 6: Mostrar totales por concepto
def mostrar_totales(lista_empleados):
    total_cesantias = sum(emp['liquidacion']['cesantias'] for emp in lista_empleados)
    total_intereses = sum(emp['liquidacion']['intereses'] for emp in lista_empleados)
    total_prima = sum(emp['liquidacion']['prima'] for emp in lista_empleados)
    total_vacaciones = sum(emp['liquidacion']['vacaciones'] for emp in lista_empleados)

    print("\n📊 Totales generales por concepto:")
    print(f"Total Cesantías: ${total_cesantias:,.2f}")
    print(f"Total Intereses: ${total_intereses:,.2f}")
    print(f"Total Prima:     ${total_prima:,.2f}")
    print(f"Total Vacaciones:${total_vacaciones:,.2f}")

# Función principal
def ingreso_masivo():
    empleados = []

    while True:
        empleado = registrar_empleado()

        # Calcular días y liquidación
        dias = (empleado['fecha_salida'] - empleado['fecha_ingreso']).days
        liquidacion = calcular_liquidacion(empleado['salario'], dias)

        # Agregar datos calculados al empleado
        empleado['dias_trabajados'] = dias
        empleado['liquidacion'] = liquidacion

        empleados.append(empleado)

        continuar = input("¿Deseas ingresar otro empleado? (s/n): ").strip().lower()
        if continuar != 's':
            break

    # Mostrar resumen
    print("\n📋 Lista de empleados ingresados:")
    for i, emp in enumerate(empleados, 1):
        print(f"\nEmpleado #{i}")
        print(f"Nombre: {emp['nombre']}")
        print(f"Edad: {emp['edad']}")
        print(f"Ingreso: {emp['fecha_ingreso'].strftime('%Y-%m-%d')}")
        print(f"Salida: {emp['fecha_salida'].strftime('%Y-%m-%d')}")
        print(f"Días trabajados: {emp['dias_trabajados']}")
        print(f"Salario: ${emp['salario']:,.2f}")
        print(f"  Cesantías: ${emp['liquidacion']['cesantias']:,.2f}")
        print(f"  Intereses: ${emp['liquidacion']['intereses']:,.2f}")
        print(f"  Prima:     ${emp['liquidacion']['prima']:,.2f}")
        print(f"  Vacaciones:${emp['liquidacion']['vacaciones']:,.2f}")

    # Guardar en archivos
    guardar_en_archivo_txt(empleados)
    guardar_en_archivo_csv(empleados)
    mostrar_totales(empleados)

    print("\n✅ Archivos 'personal.txt' y 'personal.csv' actualizados correctamente.")
    return empleados

# Ejecutar
empleados = ingreso_masivo()

ver_archivo = input("\n¿Deseas ver el contenido guardado en 'personal.txt'? (s/n): ").strip().lower()
if ver_archivo == 's':
    leer_archivo_txt()