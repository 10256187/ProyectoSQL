import tkinter as tk
from tkinter import ttk, messagebox
import crud_db  # Importa tu lógica de base de datos

class AppInsumos:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Insumos - Licitaciones")
        self.root.geometry("700x500")

        # ====== FRAME FORMULARIO ======
        frame_form = tk.LabelFrame(root, text="Datos del Insumo", padx=10, pady=10)
        frame_form.pack(fill="x", padx=10, pady=5)

        tk.Label(frame_form, text="Código:").grid(row=0, column=0, sticky="w")
        tk.Label(frame_form, text="Descripción:").grid(row=1, column=0, sticky="w")
        tk.Label(frame_form, text="Unidad:").grid(row=2, column=0, sticky="w")
        tk.Label(frame_form, text="Precio:").grid(row=3, column=0, sticky="w")

        self.codigo_entry = tk.Entry(frame_form)
        self.descripcion_entry = tk.Entry(frame_form)
        self.unidad_entry = tk.Entry(frame_form)
        self.precio_entry = tk.Entry(frame_form)

        self.codigo_entry.grid(row=0, column=1, padx=5, pady=2)
        self.descripcion_entry.grid(row=1, column=1, padx=5, pady=2)
        self.unidad_entry.grid(row=2, column=1, padx=5, pady=2)
        self.precio_entry.grid(row=3, column=1, padx=5, pady=2)

        # ====== BOTONES ======
        frame_btns = tk.Frame(root)
        frame_btns.pack(fill="x", padx=10, pady=5)

        tk.Button(frame_btns, text="Agregar", command=self.agregar).pack(side="left", padx=5)
        tk.Button(frame_btns, text="Editar", command=self.editar).pack(side="left", padx=5)
        tk.Button(frame_btns, text="Eliminar", command=self.eliminar).pack(side="left", padx=5)
        tk.Button(frame_btns, text="Actualizar", command=self.mostrar).pack(side="left", padx=5)

        # ====== TABLA ======
        frame_tabla = tk.Frame(root)
        frame_tabla.pack(fill="both", expand=True, padx=10, pady=10)

        columnas = ("codigo", "descripcion", "unidad", "precio")
        self.tree = ttk.Treeview(frame_tabla, columns=columnas, show="headings")

        for col in columnas:
            self.tree.heading(col, text=col.capitalize())
            self.tree.column(col, width=150)

        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.seleccionar)

        self.mostrar()

    # ===================== FUNCIONES =====================
    def limpiar_campos(self):
        self.codigo_entry.delete(0, tk.END)
        self.descripcion_entry.delete(0, tk.END)
        self.unidad_entry.delete(0, tk.END)
        self.precio_entry.delete(0, tk.END)

    def mostrar(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        insumos = crud_db.ver_insumos()
        for insumo in insumos:
            self.tree.insert("", tk.END, values=insumo)

    def agregar(self):
        codigo = self.codigo_entry.get()
        descripcion = self.descripcion_entry.get()
        unidad = self.unidad_entry.get()
        precio = self.precio_entry.get()

        if codigo and descripcion and unidad and precio:
            crud_db.agregar_insumo(codigo, descripcion, unidad, float(precio))
            messagebox.showinfo("Éxito", "Insumo agregado correctamente")
            self.mostrar()
            self.limpiar_campos()
        else:
            messagebox.showwarning("Error", "Todos los campos son obligatorios")

    def seleccionar(self, event):
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected[0])
            codigo, descripcion, unidad, precio = item["values"]
            self.limpiar_campos()
            self.codigo_entry.insert(0, codigo)
            self.descripcion_entry.insert(0, descripcion)
            self.unidad_entry.insert(0, unidad)
            self.precio_entry.insert(0, precio)

    def editar(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Error", "Seleccione un insumo")
            return

        codigo = self.codigo_entry.get()
        descripcion = self.descripcion_entry.get()
        unidad = self.unidad_entry.get()
        precio = self.precio_entry.get()

        if codigo and descripcion and unidad and precio:
            crud_db.editar_insumo(codigo, descripcion, unidad, float(precio))
            messagebox.showinfo("Éxito", "Insumo actualizado")
            self.mostrar()
            self.limpiar_campos()
        else:
            messagebox.showwarning("Error", "Todos los campos son obligatorios")

    def eliminar(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Error", "Seleccione un insumo")
            return
        item = self.tree.item(selected[0])
        codigo = item["values"][0]

        crud_db.eliminar_insumo(codigo)
        messagebox.showinfo("Éxito", "Insumo eliminado")
        self.mostrar()
        self.limpiar_campos()


if __name__ == "__main__":
    root = tk.Tk()
    app = AppInsumos(root)
    root.mainloop()