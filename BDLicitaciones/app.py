from gestores import (GestorMaterialesSQLite, GestorManoObraSQLite, GestorHerramientasSQLite, GestorTransporteSQLite)

def menu():
    gestor_material = GestorMaterialesSQLite()
    gestor_mano_obra = GestorManoObraSQLite()
    gestor_herramientas = GestorHerramientasSQLite()
    gestor_transporte = GestorTransporteSQLite()


    while True:
        print("\n📋 Menú Principal")
        print("1. Gestion Materiales")
        print("2. Gestion Mano de obra")
        print("3. Gestion Herramienta")
        print("4. Gestion Transpote")
        print("5. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            gestionar_materiales(gestor_material)
        elif opcion =="2":
            gestionar_mano_obra(gestor_mano_obra)
        elif opcion =="3":
            gestionar_herramienta(gestor_herramientas)
        elif opcion =="4":
            gestionar_transporte(gestor_transporte)
        elif opcion == "5":
            print("👋 Hasta luego.")
            break
        else:
            print("❌ Opción no válida.")

def gestionar_materiales(gestor):
    while True:
        print("\n🔧 Gestión de Materiales")
        print("1. Agregar")
        print("2. Ver materiales")
        print("3. Editar material")
        print("4. Volver")
        opcion = input("Opción: ")

        if opcion == "1":
            gestor.agregar_material()
        elif opcion == "2":
            gestor.ver_materiales()
        elif opcion == "3":
            gestor.editar_material()
        elif opcion == "4":
            break

def gestionar_mano_obra(gestor):
    while True:
        print("\n🔧 Gestión Mano de obra")
        print("1. Agregar mano de obra")
        print("2. Ver mano de obra")
        print("3. Editar costos de mano de obra")
        print("4. Volver")
        opcion = input("Opción: ")

        if opcion == "1":
            gestor.agregar_mano_obra()
        elif opcion == "2":
            gestor.ver_mano_obra()
        elif opcion == "3":
            gestor.editar_mano_obra()
        elif opcion == "4":
            break
        
def gestionar_herramienta(gestor):
    while True:
        print("\n🔧 Gestión herramienta")
        print("1. Agregar herramienta")
        print("2. Ver Herramienta")
        print("3. Editar costo herramienta")
        print("4. Volver")
        opcion = input("Opción: ")

        if opcion == "1":
            gestor.agregar_herramienta()
        elif opcion == "2":
            gestor.ver_herramientas()
        elif opcion == "3":
            gestor.editar_herramienta()
        elif opcion == "4":
            break


def gestionar_transporte(gestor):
    while True:
        print("\n🔧 Gestión transporte")
        print("1. Agregar transporte")
        print("2. Ver transport")
        print("3. Editar costo transporte")
        print("4. Volver")
        opcion = input("Opción: ")

        if opcion == "1":
            gestor.agregar_transporte()
        elif opcion == "2":
            gestor.ver_transporte()
        elif opcion == "3":
            gestor.editar_transporte()
        elif opcion == "4":
            break

if __name__ == "__main__":
    menu()