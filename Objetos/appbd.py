from BDPrimaria import GestorMateriales

def mostrar_menu():
    print("\n📦 MENÚ DE MATERIALES")
    print("1. Agregar material")
    print("2. Ver todos los materiales")
    print("3. Editar material")
    print("4. Eliminar material")  # <-- Nueva línea
    print("5. Salir")


if __name__ == "__main__":
    gestor = GestorMateriales()

    while True:
        mostrar_menu()
        opcion = input("Selecciona una opción: ").strip()

        if opcion == "1":
            gestor.agregar_material()
        elif opcion == "2":
            gestor.mostrar_todos()
        elif opcion == "3":
            gestor.editar_material()
        elif opcion == "4":
            gestor.eliminar_material()  # <-- Nueva línea
        elif opcion == "5":
            print("👋 Hasta luego.")
            break
        else:
            print("❌ Opción no válida.")