import json
import os
import re

class Material:
    def __init__(self, codigo, descripcion, unidad, precio, peso):
        self.codigo = codigo
        self.descripcion = descripcion
        self.unidad = unidad
        self.precio = precio
        self.peso = peso

    def __str__(self):
        return f"{self.codigo} | {self.descripcion} | {self.unidad} | ${self.precio} | {self.peso}kg"

    def a_diccionario(self):
        return {
            "codigo": self.codigo,
            "descripcion": self.descripcion,
            "unidad": self.unidad,
            "precio": self.precio,
            "peso": self.peso
        }

class GestorMateriales:
    def __init__(self, archivo="materiales.json"):
        self.archivo = archivo
        self.materiales = self.cargar()

    def obtener_material_por_codigo(self, codigo):
        """Devuelve el objeto Material con ese código o None si no existe."""
        for mat in self.materiales:
            if mat.codigo == codigo:
                return mat
        return None

    def cargar(self):
        if os.path.exists(self.archivo):
            with open(self.archivo, "r", encoding="utf-8") as f:
                datos_json = json.load(f)
                return [Material(**d) for d in datos_json]
        return []

    def guardar(self):
        with open(self.archivo, "w", encoding="utf-8") as f:
            json.dump([m.a_diccionario() for m in self.materiales], f, indent=4, ensure_ascii=False)

    def mostrar_todos(self):
        if not self.materiales:
            print("⚠️ No hay materiales aún.")
            return
        for m in self.materiales:
            print("🔸", m)

    def agregar_material(self):
        print("\n🟢 Agregar nuevo material")

        while True:
            cod = input("Código (formato: AAAANNNN o AAAA-NNNN): ").strip().upper()

            if re.match(r"^[A-Z]{4}\d{4}$", cod):
                cod = cod[:4] + "-" + cod[4:]

            if not re.match(r"^[A-Z]{4}-\d{4}$", cod):
                print("❌ Código inválido. Usa 4 letras, guion, 4 números (ej: ABCD-1234).")
                continue

            if any(m.codigo == cod for m in self.materiales):
                print("⚠️ Ya existe un material con ese código.")
                continue

            codigo = cod
            break

        descripcion = input("Descripción: ").strip()
        unidades_validas = ["Ml","kM","Lb","Kg","Lt","cm","mL","gL","Hz","Un","Sc","M³","M²","pg", "pt", "cñ"]
        while True:
            unidad = input("Unidad (ej: Ml, Un, m³): ").strip()

            if not re.match(r"^[A-Za-z][A-Za-z0-9]$", unidad):
                print("❌ Unidad inválida. Debe tener 2 caracteres: el primero una letra, el segundo letra o número.")
                continue
            break

        try:
            precio = float(input("Precio (ej: 2500): ").replace(",", "."))
            peso = float(input("Peso (por unidad de medida): ").replace(",", "."))
        except ValueError:
            print("❌ Error: el precio y el peso deben ser números.")
            return

        nuevo = Material(codigo, descripcion, unidad, precio, peso)
        self.materiales.append(nuevo)
        self.materiales.sort(key=lambda x: x.codigo.lower())
        self.guardar()

        print("✅ Material agregado con éxito.")
        
    def editar_material(self):
        print("\n✏️ Editar material")

        if not self.materiales:
            print("⚠️ No hay materiales para editar.")
            return

        cod_buscar = input("Código del material a editar: ").strip().upper()
        if re.match(r"^[A-Z]{4}\d{4}$", cod_buscar):
            cod_buscar = cod_buscar[:4] + "-" + cod_buscar[4:]

        material = self.obtener_material_por_codigo(cod_buscar)
        
        if not material:
            print("❌ Código no encontrado.")
            return

        print(f"\n🔍 Editando {material.codigo} - {material.descripcion}")
        
        nuevo_codigo = input(f"Código nuevo [{material.codigo}]: ").strip().upper()
        if nuevo_codigo:
            if re.match(r"^[A-Z]{4}\d{4}$", nuevo_codigo):
                nuevo_codigo = nuevo_codigo[:4] + "-" + nuevo_codigo[4:]
            if not re.match(r"^[A-Z]{4}-\d{4}$", nuevo_codigo):
                print("❌ Código inválido. Se mantiene el anterior.")
            elif self.obtener_material_por_codigo(nuevo_codigo) and nuevo_codigo != material.codigo:
                print("⚠️ Ese código ya está en uso. Se mantiene el anterior.")
            else:
                material.codigo = nuevo_codigo
        
        nueva_desc = input(f"Descripción nueva [{material.descripcion}]: ").strip()
        if nueva_desc:
            material.descripcion = nueva_desc

        nueva_unidad = input(f"Unidad nueva [{material.unidad}]: ").strip().upper()
        if nueva_unidad:
            if re.match(r"^[A-Z][A-Z0-9]$", nueva_unidad):
                material.unidad = nueva_unidad
            else:
                print("❌ Unidad inválida. Se mantiene la anterior.")

        nuevo_precio = input(f"Precio nuevo [{material.precio}]: ").replace(",", ".").strip()
        if nuevo_precio:
            try:
                material.precio = float(nuevo_precio)
            except ValueError:
                print("❌ Precio inválido. Se mantiene el anterior.")

        nuevo_peso = input(f"Peso nuevo [{material.peso}]: ").replace(",", ".").strip()
        if nuevo_peso:
            try:
                material.peso = float(nuevo_peso)
            except ValueError:
                print("❌ Peso inválido. Se mantiene el anterior.")

        self.materiales.sort(key=lambda x: x.codigo)
        self.guardar()
        print("✅ Material actualizado y reordenado por código.")

    print("❌ Código no encontrado.")

    def eliminar_material(self):
        print("\n🗑️ Eliminar material")
        if not self.materiales:
            print("⚠️ No hay materiales para eliminar.")
            return

        cod_buscar = input("Ingrese el código del material a eliminar: ").strip().upper()
        if re.match(r"^[A-Z]{4}\d{4}$", cod_buscar):
            cod_buscar = cod_buscar[:4] + "-" + cod_buscar[4:]

        material = self.obtener_material_por_codigo(cod_buscar)

        if not material:
            print("❌ Código no encontrado.")
            return

        print(f"🧾 Se eliminará: {material}")
        confirmacion = input("¿Está seguro? (s/n): ").strip().lower()

        if confirmacion == "s":
            self.materiales.remove(material)
            self.guardar()
            print("✅ Material eliminado con éxito.")
        else:
            print("❌ Cancelado por el usuario.")