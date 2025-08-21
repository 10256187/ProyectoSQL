from base_datos import crear_tabla, conectar, agregar_insumo, ver_materiales, editar_material, eliminar_material

def mostrar_menu():
    print("\n===== Gestor archivo maestro de materiales (.db) =====")
    print("1. Agregar material")
    print("2. Ver materiales")
    print("3. Editar Insumos")
    print("4. Eliminar Insumos")
    print("5. Salir")

def main():
    crear_tabla()
    while True:
        mostrar_menu()
        opcion = input("Elige una opción: ").strip()
        if opcion == "1":
            conn = conectar()
            cursor = conn.cursor()
            agregar_insumo(cursor, conn)
            conn.close()
        elif opcion == "2":
            ver_materiales()
        elif opcion == "3":
            editar_material()
        elif opcion == "4":
            eliminar_material()
        elif opcion == "5":
            print("💾 Guardando y saliendo... ¡Hasta luego!")
            break
        else:
            print("❌ Opción inválida.")

if __name__ == "__main__":
    main()