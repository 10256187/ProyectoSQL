from BDSQlite import GestorMaterialesSQLite

if __name__ == "__main__":
    gestor = GestorMaterialesSQLite()

    while True:
        print("\n📦 GESTOR DE MATERIALES")
        print("1. Agregar material")
        print("2. Ver materiales")
        print("3. Editar material")
        print("4. Eliminar material")
        print("5. Buscar material")
        print("6. Salir")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            gestor.agregar_material()
        elif opcion == "2":
            gestor.ver_materiales()
        elif opcion == "3":
            gestor.editar_material()
        elif opcion == "4":
            gestor.eliminar_material()
        elif opcion == "5":
            gestor.buscar_material()
        elif opcion == "6":
            print("👋 Saliendo del programa.")
            break
        else:
            print("❌ Opción no válida. Intente de nuevo.")