# presentacion.py
import tkinter as tk
from tkinter import ttk, messagebox
from crud_db import (
    crear_material, leer_materiales, actualizar_material,
    crear_mobra, leer_mobra, actualizar_mobra,
    crear_herramienta, leer_herramientas, actualizar_herramienta,
    crear_transporte, leer_transporte, actualizar_transporte,
    crear_unitario, leer_unitarios, crear_componente_unitario, leer_componentes_unitario
)

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestor de Presupuestos")
        self.root.geometry("1000x700")

        # Crear el NoteBook para las pestañas
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(pady=10, expand=True, fill="both")

        # Crear pestañas
        self.tab_materiales = ttk.Frame(self.notebook)
        self.tab_mobra = ttk.Frame(self.notebook)
        self.tab_herramientas = ttk.Frame(self.notebook)
        self.tab_transporte = ttk.Frame(self.notebook)
        self.tab_unitarios = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_materiales, text="Materiales")
        self.notebook.add(self.tab_mobra, text="Mano de Obra")
        self.notebook.add(self.tab_herramientas, text="Herramientas")
        self.notebook.add(self.tab_transporte, text="Transporte")
        self.notebook.add(self.tab_unitarios, text="Análisis Unitario")

        # Configurar pestañas
        self.setup_materiales_tab()
        self.setup_mobra_tab()
        self.setup_herramientas_tab()
        self.setup_transporte_tab()
        self.setup_unitarios_tab()

    # ====================================================================
    # --- Configuración de Pestaña de Materiales ---
    # ====================================================================
    def setup_materiales_tab(self):
        # Frame para la entrada de datos (arriba)
        frame_input = ttk.LabelFrame(self.tab_materiales, text="Crear/Actualizar Material")
        frame_input.pack(padx=10, pady=10, fill="x")

        # Etiquetas y campos de entrada
        self.entries_material = {}
        fields = ["Código", "Descripción", "Unidad", "Precio", "Peso", "Tipo"]
        for i, field in enumerate(fields):
            label = ttk.Label(frame_input, text=f"{field}:")
            label.grid(row=i, column=0, padx=5, pady=2, sticky="e")
            entry = ttk.Entry(frame_input)
            entry.grid(row=i, column=1, padx=5, pady=2, sticky="we")
            self.entries_material[field] = entry

        frame_input.columnconfigure(1, weight=1)

        # Botones
        frame_buttons = ttk.Frame(frame_input)
        frame_buttons.grid(row=len(fields), column=0, columnspan=2, pady=10)

        btn_crear = ttk.Button(frame_buttons, text="Crear", command=self.crear_material)
        btn_crear.pack(side="left", padx=5)

        btn_actualizar = ttk.Button(frame_buttons, text="Actualizar", command=self.actualizar_material)
        btn_actualizar.pack(side="left", padx=5)

        # Separador
        ttk.Separator(self.tab_materiales, orient="horizontal").pack(fill="x", pady=10)

        # Treeview para mostrar los materiales (abajo)
        self.tree_material = ttk.Treeview(self.tab_materiales, columns=fields, show="headings")
        self.tree_material.pack(padx=10, pady=10, expand=True, fill="both")

        for field in fields:
            self.tree_material.heading(field, text=field)
            self.tree_material.column(field, width=100)

        # Cuando el usuario selecciona una fila, carga los datos en los campos de entrada
        self.tree_material.bind("<<TreeviewSelect>>", self.cargar_material)
        # ESTA LÍNEA ES LA QUE CARGA LOS MATERIALES AL INICIAR LA PESTAÑA
        self.actualizar_materiales_treeview()

    def actualizar_materiales_treeview(self):
        # Borrar datos existentes
        for row in self.tree_material.get_children():
            self.tree_material.delete(row)

        # Insertar nuevos datos
        materiales = leer_materiales()
        for mat in materiales:
            self.tree_material.insert("", "end", values=mat)

    def crear_material(self):
        try:
            codigo = self.entries_material['Código'].get()
            descripcion = self.entries_material['Descripción'].get()
            unidad = self.entries_material['Unidad'].get()
            precio = float(self.entries_material['Precio'].get())
            peso = float(self.entries_material['Peso'].get())
            tipo = self.entries_material['Tipo'].get()

            if not all([codigo, descripcion, unidad, tipo]):
                messagebox.showwarning("Advertencia", "Todos los campos (excepto los numéricos) deben estar llenos.")
                return

            crear_material(codigo, descripcion, unidad, precio, peso, tipo)
            self.actualizar_materiales_treeview()
            messagebox.showinfo("Éxito", "Material creado correctamente.")
        except ValueError:
            messagebox.showerror("Error", "Los campos 'Precio' y 'Peso' deben ser números.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")

    def actualizar_material(self):
        selected_item = self.tree_material.focus()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Por favor, seleccione un material para actualizar.")
            return

        try:
            codigo = self.tree_material.item(selected_item)["values"][0]
            nueva_descripcion = self.entries_material['Descripción'].get()
            nueva_unidad = self.entries_material['Unidad'].get()
            nuevo_precio = float(self.entries_material['Precio'].get())
            nuevo_peso = float(self.entries_material['Peso'].get())
            nuevo_tipo = self.entries_material['Tipo'].get()

            if not all([nueva_descripcion, nueva_unidad, nuevo_tipo]):
                messagebox.showwarning("Advertencia", "Todos los campos (excepto los numéricos) deben estar llenos.")
                return

            actualizar_material(codigo, nueva_descripcion, nueva_unidad, nuevo_precio, nuevo_peso, nuevo_tipo)
            self.actualizar_materiales_treeview()
            messagebox.showinfo("Éxito", "Material actualizado correctamente.")
        except ValueError:
            messagebox.showerror("Error", "Los campos 'Precio' y 'Peso' deben ser números.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")

    def cargar_material(self, event):
        selected_item = self.tree_material.focus()
        if selected_item:
            values = self.tree_material.item(selected_item)["values"]
            fields = ["Código", "Descripción", "Unidad", "Precio", "Peso", "Tipo"]
            for i, field in enumerate(fields):
                self.entries_material[field].delete(0, tk.END)
                self.entries_material[field].insert(0, values[i])

    # ====================================================================
    # --- Configuración de Pestaña de Mano de Obra ---
    # ====================================================================
    def setup_mobra_tab(self):
        # Frame para la entrada de datos (arriba)
        frame_input = ttk.LabelFrame(self.tab_mobra, text="Crear/Actualizar Mano de Obra")
        frame_input.pack(padx=10, pady=10, fill="x")

        # Etiquetas y campos de entrada
        self.entries_mobra = {}
        fields = ["Código", "Descripción", "Unidad", "Precio"]
        for i, field in enumerate(fields):
            label = ttk.Label(frame_input, text=f"{field}:")
            label.grid(row=i, column=0, padx=5, pady=2, sticky="e")
            entry = ttk.Entry(frame_input)
            entry.grid(row=i, column=1, padx=5, pady=2, sticky="we")
            self.entries_mobra[field] = entry

        frame_input.columnconfigure(1, weight=1)

        # Botones
        frame_buttons = ttk.Frame(frame_input)
        frame_buttons.grid(row=len(fields), column=0, columnspan=2, pady=10)

        btn_crear = ttk.Button(frame_buttons, text="Crear", command=self.crear_mobra)
        btn_crear.pack(side="left", padx=5)

        btn_actualizar = ttk.Button(frame_buttons, text="Actualizar", command=self.actualizar_mobra)
        btn_actualizar.pack(side="left", padx=5)

        # Separador
        ttk.Separator(self.tab_mobra, orient="horizontal").pack(fill="x", pady=10)

        # Treeview para mostrar la mano de obra (abajo)
        self.tree_mobra = ttk.Treeview(self.tab_mobra, columns=fields, show="headings")
        self.tree_mobra.pack(padx=10, pady=10, expand=True, fill="both")

        for field in fields:
            self.tree_mobra.heading(field, text=field)
            self.tree_mobra.column(field, width=100)

        self.tree_mobra.bind("<<TreeviewSelect>>", self.cargar_mobra)
        self.actualizar_mobra_treeview()

    def actualizar_mobra_treeview(self):
        for row in self.tree_mobra.get_children():
            self.tree_mobra.delete(row)

        mobra = leer_mobra()
        for mob in mobra:
            self.tree_mobra.insert("", "end", values=mob)

    def crear_mobra(self):
        try:
            codigo = self.entries_mobra['Código'].get()
            descripcion = self.entries_mobra['Descripción'].get()
            unidad = self.entries_mobra['Unidad'].get()
            precio = float(self.entries_mobra['Precio'].get())

            if not all([codigo, descripcion, unidad, precio]):
                messagebox.showwarning("Advertencia", "Todos los campos deben estar llenos.")
                return

            crear_mobra(codigo, descripcion, unidad, precio)
            self.actualizar_mobra_treeview()
            messagebox.showinfo("Éxito", "Mano de obra creada correctamente.")
        except ValueError:
            messagebox.showerror("Error", "El campo 'Precio' debe ser un número.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")

    def actualizar_mobra(self):
        selected_item = self.tree_mobra.focus()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Por favor, seleccione una mano de obra para actualizar.")
            return

        try:
            codigo = self.tree_mobra.item(selected_item)["values"][0]
            nueva_descripcion = self.entries_mobra['Descripción'].get()
            nueva_unidad = self.entries_mobra['Unidad'].get()
            nuevo_precio = float(self.entries_mobra['Precio'].get())

            if not all([nueva_descripcion, nueva_unidad, nuevo_precio]):
                messagebox.showwarning("Advertencia", "Todos los campos deben estar llenos.")
                return

            actualizar_mobra(codigo, nueva_descripcion, nueva_unidad, nuevo_precio)
            self.actualizar_mobra_treeview()
            messagebox.showinfo("Éxito", "Mano de obra actualizada correctamente.")
        except ValueError:
            messagebox.showerror("Error", "El campo 'Precio' debe ser un número.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")

    def cargar_mobra(self, event):
        selected_item = self.tree_mobra.focus()
        if selected_item:
            values = self.tree_mobra.item(selected_item)["values"]
            fields = ["Código", "Descripción", "Unidad", "Precio"]
            for i, field in enumerate(fields):
                self.entries_mobra[field].delete(0, tk.END)
                self.entries_mobra[field].insert(0, values[i])

    # ====================================================================
    # --- Configuración de Pestaña de Herramientas ---
    # ====================================================================
    def setup_herramientas_tab(self):
        # Frame para la entrada de datos (arriba)
        frame_input = ttk.LabelFrame(self.tab_herramientas, text="Crear/Actualizar Herramienta")
        frame_input.pack(padx=10, pady=10, fill="x")

        self.entries_herramienta = {}
        fields = ["Código", "Descripción", "Unidad", "Precio"]
        for i, field in enumerate(fields):
            label = ttk.Label(frame_input, text=f"{field}:")
            label.grid(row=i, column=0, padx=5, pady=2, sticky="e")
            entry = ttk.Entry(frame_input)
            entry.grid(row=i, column=1, padx=5, pady=2, sticky="we")
            self.entries_herramienta[field] = entry

        frame_input.columnconfigure(1, weight=1)

        frame_buttons = ttk.Frame(frame_input)
        frame_buttons.grid(row=len(fields), column=0, columnspan=2, pady=10)

        btn_crear = ttk.Button(frame_buttons, text="Crear", command=self.crear_herramienta)
        btn_crear.pack(side="left", padx=5)

        btn_actualizar = ttk.Button(frame_buttons, text="Actualizar", command=self.actualizar_herramienta)
        btn_actualizar.pack(side="left", padx=5)

        # Separador
        ttk.Separator(self.tab_herramientas, orient="horizontal").pack(fill="x", pady=10)

        # Treeview para mostrar las herramientas (abajo)
        self.tree_herramienta = ttk.Treeview(self.tab_herramientas, columns=fields, show="headings")
        self.tree_herramienta.pack(padx=10, pady=10, expand=True, fill="both")

        for field in fields:
            self.tree_herramienta.heading(field, text=field)
            self.tree_herramienta.column(field, width=100)

        self.tree_herramienta.bind("<<TreeviewSelect>>", self.cargar_herramienta)
        self.actualizar_herramientas_treeview()

    def actualizar_herramientas_treeview(self):
        for row in self.tree_herramienta.get_children():
            self.tree_herramienta.delete(row)

        herramientas = leer_herramientas()
        for herr in herramientas:
            self.tree_herramienta.insert("", "end", values=herr)

    def crear_herramienta(self):
        try:
            codigo = self.entries_herramienta['Código'].get()
            descripcion = self.entries_herramienta['Descripción'].get()
            unidad = self.entries_herramienta['Unidad'].get()
            precio = float(self.entries_herramienta['Precio'].get())

            if not all([codigo, descripcion, unidad, precio]):
                messagebox.showwarning("Advertencia", "Todos los campos deben estar llenos.")
                return

            crear_herramienta(codigo, descripcion, unidad, precio)
            self.actualizar_herramientas_treeview()
            messagebox.showinfo("Éxito", "Herramienta creada correctamente.")
        except ValueError:
            messagebox.showerror("Error", "El campo 'Precio' debe ser un número.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")

    def actualizar_herramienta(self):
        selected_item = self.tree_herramienta.focus()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Por favor, seleccione una herramienta para actualizar.")
            return

        try:
            codigo = self.tree_herramienta.item(selected_item)["values"][0]
            nueva_descripcion = self.entries_herramienta['Descripción'].get()
            nueva_unidad = self.entries_herramienta['Unidad'].get()
            nuevo_precio = float(self.entries_herramienta['Precio'].get())

            if not all([nueva_descripcion, nueva_unidad, nuevo_precio]):
                messagebox.showwarning("Advertencia", "Todos los campos deben estar llenos.")
                return

            actualizar_herramienta(codigo, nueva_descripcion, nueva_unidad, nuevo_precio)
            self.actualizar_herramientas_treeview()
            messagebox.showinfo("Éxito", "Herramienta actualizada correctamente.")
        except ValueError:
            messagebox.showerror("Error", "El campo 'Precio' debe ser un número.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")

    def cargar_herramienta(self, event):
        selected_item = self.tree_herramienta.focus()
        if selected_item:
            values = self.tree_herramienta.item(selected_item)["values"]
            fields = ["Código", "Descripción", "Unidad", "Precio"]
            for i, field in enumerate(fields):
                self.entries_herramienta[field].delete(0, tk.END)
                self.entries_herramienta[field].insert(0, values[i])

    # ====================================================================
    # --- Configuración de Pestaña de Transporte ---
    # ====================================================================
    def setup_transporte_tab(self):
        # Frame para la entrada de datos (arriba)
        frame_input = ttk.LabelFrame(self.tab_transporte, text="Crear/Actualizar Transporte")
        frame_input.pack(padx=10, pady=10, fill="x")

        self.entries_transporte = {}
        fields = ["Código", "Descripción", "Unidad", "Precio"]
        for i, field in enumerate(fields):
            label = ttk.Label(frame_input, text=f"{field}:")
            label.grid(row=i, column=0, padx=5, pady=2, sticky="e")
            entry = ttk.Entry(frame_input)
            entry.grid(row=i, column=1, padx=5, pady=2, sticky="we")
            self.entries_transporte[field] = entry

        frame_input.columnconfigure(1, weight=1)

        frame_buttons = ttk.Frame(frame_input)
        frame_buttons.grid(row=len(fields), column=0, columnspan=2, pady=10)

        btn_crear = ttk.Button(frame_buttons, text="Crear", command=self.crear_transporte)
        btn_crear.pack(side="left", padx=5)

        btn_actualizar = ttk.Button(frame_buttons, text="Actualizar", command=self.actualizar_transporte)
        btn_actualizar.pack(side="left", padx=5)

        # Separador
        ttk.Separator(self.tab_transporte, orient="horizontal").pack(fill="x", pady=10)

        # Treeview para mostrar el transporte (abajo)
        self.tree_transporte = ttk.Treeview(self.tab_transporte, columns=fields, show="headings")
        self.tree_transporte.pack(padx=10, pady=10, expand=True, fill="both")

        for field in fields:
            self.tree_transporte.heading(field, text=field)
            self.tree_transporte.column(field, width=100)

        self.tree_transporte.bind("<<TreeviewSelect>>", self.cargar_transporte)
        self.actualizar_transporte_treeview()

    def actualizar_transporte_treeview(self):
        for row in self.tree_transporte.get_children():
            self.tree_transporte.delete(row)

        transportes = leer_transporte()
        for trans in transportes:
            self.tree_transporte.insert("", "end", values=trans)

    def crear_transporte(self):
        try:
            codigo = self.entries_transporte['Código'].get()
            descripcion = self.entries_transporte['Descripción'].get()
            unidad = self.entries_transporte['Unidad'].get()
            precio = float(self.entries_transporte['Precio'].get())

            if not all([codigo, descripcion, unidad, precio]):
                messagebox.showwarning("Advertencia", "Todos los campos deben estar llenos.")
                return

            crear_transporte(codigo, descripcion, unidad, precio)
            self.actualizar_transporte_treeview()
            messagebox.showinfo("Éxito", "Transporte creado correctamente.")
        except ValueError:
            messagebox.showerror("Error", "El campo 'Precio' debe ser un número.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")

    def actualizar_transporte(self):
        selected_item = self.tree_transporte.focus()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Por favor, seleccione un transporte para actualizar.")
            return

        try:
            codigo = self.tree_transporte.item(selected_item)["values"][0]
            nueva_descripcion = self.entries_transporte['Descripción'].get()
            nueva_unidad = self.entries_transporte['Unidad'].get()
            nuevo_precio = float(self.entries_transporte['Precio'].get())

            if not all([nueva_descripcion, nueva_unidad, nuevo_precio]):
                messagebox.showwarning("Advertencia", "Todos los campos deben estar llenos.")
                return

            actualizar_transporte(codigo, nueva_descripcion, nueva_unidad, nuevo_precio)
            self.actualizar_transporte_treeview()
            messagebox.showinfo("Éxito", "Transporte actualizado correctamente.")
        except ValueError:
            messagebox.showerror("Error", "El campo 'Precio' debe ser un número.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")

    def cargar_transporte(self, event):
        selected_item = self.tree_transporte.focus()
        if selected_item:
            values = self.tree_transporte.item(selected_item)["values"]
            fields = ["Código", "Descripción", "Unidad", "Precio"]
            for i, field in enumerate(fields):
                self.entries_transporte[field].delete(0, tk.END)
                self.entries_transporte[field].insert(0, values[i])

    # ====================================================================
    # --- Configuración de Pestaña de Análisis Unitario ---
    # ====================================================================
    def setup_unitarios_tab(self):
        # Frame de la izquierda para crear/seleccionar unitarios
        frame_left = ttk.Frame(self.tab_unitarios)
        frame_left.pack(side="left", padx=10, pady=10, fill="y", expand=False)

        # Frame de la derecha para gestionar componentes
        frame_right = ttk.Frame(self.tab_unitarios)
        frame_right.pack(side="right", padx=10, pady=10, fill="both", expand=True)

        # Sección para crear un nuevo unitario (Usando grid para consistencia)
        frame_crear_unitario = ttk.LabelFrame(frame_left, text="Crear Nuevo Análisis Unitario")
        frame_crear_unitario.pack(pady=10, fill="x")

        # Código
        ttk.Label(frame_crear_unitario, text="Código:").grid(row=0, column=0, padx=5, pady=2, sticky="w")
        self.entry_unitario_codigo = ttk.Entry(frame_crear_unitario)
        self.entry_unitario_codigo.grid(row=0, column=1, padx=5, pady=2, sticky="we")

        # Descripción
        ttk.Label(frame_crear_unitario, text="Descripción:").grid(row=1, column=0, padx=5, pady=2, sticky="w")
        self.entry_unitario_desc = ttk.Entry(frame_crear_unitario)
        self.entry_unitario_desc.grid(row=1, column=1, padx=5, pady=2, sticky="we")

        # Unidad
        ttk.Label(frame_crear_unitario, text="Unidad:").grid(row=2, column=0, padx=5, pady=2, sticky="w")
        self.entry_unitario_unidad = ttk.Entry(frame_crear_unitario)
        self.entry_unitario_unidad.grid(row=2, column=1, padx=5, pady=2, sticky="we")

        btn_crear_unitario = ttk.Button(frame_crear_unitario, text="Crear Unitario", command=self.crear_unitario)
        btn_crear_unitario.grid(row=3, column=0, columnspan=2, pady=5, sticky="ew")

        frame_crear_unitario.columnconfigure(1, weight=1)

        # Sección para seleccionar un unitario existente
        frame_seleccionar_unitario = ttk.LabelFrame(frame_left, text="Seleccionar Análisis Unitario")
        frame_seleccionar_unitario.pack(pady=10, fill="both", expand=True)

        fields_unitarios = ["Código", "Descripción"]
        self.tree_unitarios = ttk.Treeview(frame_seleccionar_unitario, columns=fields_unitarios, show="headings")
        self.tree_unitarios.pack(padx=5, pady=5, expand=True, fill="both")

        for field in fields_unitarios:
            self.tree_unitarios.heading(field, text=field)
            self.tree_unitarios.column(field, width=100)

        self.tree_unitarios.bind("<<TreeviewSelect>>", self.cargar_componentes_unitario)
        self.actualizar_unitarios_treeview()

        # Sección de componentes del unitario (lado derecho)
        self.frame_componentes = ttk.LabelFrame(frame_right, text="Componentes del Análisis Unitario")
        self.frame_componentes.pack(fill="both", expand=True, padx=10, pady=10)
        self.frame_componentes.columnconfigure(1, weight=1)

        # Combobox para seleccionar tipo de componente (Usando grid ahora)
        ttk.Label(self.frame_componentes, text="Tipo de Componente:").grid(row=0, column=0, padx=5, pady=2, sticky="w")
        self.component_type_var = tk.StringVar()
        self.component_type_combo = ttk.Combobox(self.frame_componentes, textvariable=self.component_type_var,
                                                 values=["material", "mobra", "herramienta", "transporte"])
        self.component_type_combo.grid(row=0, column=1, padx=5, pady=2, sticky="we")
        self.component_type_combo.bind("<<ComboboxSelected>>", self.actualizar_componentes_combo)

        # Combobox para seleccionar el componente (Usando grid ahora)
        ttk.Label(self.frame_componentes, text="Seleccionar Componente:").grid(row=1, column=0, padx=5, pady=2, sticky="w")
        self.component_combo_var = tk.StringVar()
        self.component_combo = ttk.Combobox(self.frame_componentes, textvariable=self.component_combo_var)
        self.component_combo.grid(row=1, column=1, padx=5, pady=2, sticky="we")

        # Entrada para la cantidad (Usando grid ahora)
        ttk.Label(self.frame_componentes, text="Cantidad:").grid(row=2, column=0, padx=5, pady=2, sticky="w")
        self.entry_cantidad_componente = ttk.Entry(self.frame_componentes)
        self.entry_cantidad_componente.grid(row=2, column=1, padx=5, pady=2, sticky="we")

        # Botón para añadir componente (Usando grid ahora)
        btn_add_componente = ttk.Button(self.frame_componentes, text="Añadir Componente", command=self.agregar_componente_a_unitario)
        btn_add_componente.grid(row=3, column=0, columnspan=2, pady=10, sticky="ew")

        # Treeview para mostrar los componentes del unitario
        self.tree_componentes = ttk.Treeview(self.frame_componentes, columns=("Tipo", "Código", "Descripción", "Unidad", "Precio", "Cantidad"), show="headings")
        self.tree_componentes.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

        # Configurar el grid para que el treeview se expanda
        self.frame_componentes.grid_rowconfigure(4, weight=1)

        headings = {"Tipo": 80, "Código": 80, "Descripción": 200, "Unidad": 60, "Precio": 60, "Cantidad": 60}
        for col, width in headings.items():
            self.tree_componentes.heading(col, text=col)
            self.tree_componentes.column(col, width=width)

    def actualizar_unitarios_treeview(self):
        for row in self.tree_unitarios.get_children():
            self.tree_unitarios.delete(row)

        unitarios = leer_unitarios()
        for uni in unitarios:
            self.tree_unitarios.insert("", "end", values=(uni[0], uni[1]))

    def crear_unitario(self):
        codigo = self.entry_unitario_codigo.get()
        descripcion = self.entry_unitario_desc.get()
        unidad = self.entry_unitario_unidad.get()

        if codigo and descripcion and unidad:
            try:
                crear_unitario(codigo, descripcion, unidad)
                self.actualizar_unitarios_treeview()
                messagebox.showinfo("Éxito", "Análisis unitario creado correctamente.")
                self.entry_unitario_codigo.delete(0, tk.END)
                self.entry_unitario_desc.delete(0, tk.END)
                self.entry_unitario_unidad.delete(0, tk.END)
            except Exception as e:
                messagebox.showerror("Error", f"Error al crear el unitario: {e}")
        else:
            messagebox.showwarning("Advertencia", "Por favor, complete todos los campos para el unitario.")

    def actualizar_componentes_combo(self, event):
        tipo = self.component_type_var.get()
        self.component_combo.set('')

        if tipo == "material":
            data = leer_materiales()
        elif tipo == "mobra":
            data = leer_mobra()
        elif tipo == "herramienta":
            data = leer_herramientas()
        elif tipo == "transporte":
            data = leer_transporte()
        else:
            data = []

        codigos = [item[0] for item in data]
        self.component_combo['values'] = codigos

    def agregar_componente_a_unitario(self):
        selected_unitario = self.tree_unitarios.focus()
        if not selected_unitario:
            messagebox.showwarning("Advertencia", "Por favor, seleccione un análisis unitario.")
            return

        codigo_unitario = self.tree_unitarios.item(selected_item)["values"][0]
        tipo_componente = self.component_type_var.get()
        codigo_componente = self.component_combo_var.get()
        cantidad = self.entry_cantidad_componente.get()

        if tipo_componente and codigo_componente and cantidad:
            try:
                cantidad = float(cantidad)
                crear_componente_unitario(codigo_unitario, tipo_componente, codigo_componente, cantidad)
                self.cargar_componentes_unitario(None)
                messagebox.showinfo("Éxito", "Componente añadido correctamente.")
            except ValueError:
                messagebox.showerror("Error", "La cantidad debe ser un número válido.")
            except Exception as e:
                messagebox.showerror("Error", f"Error al añadir componente: {e}")
        else:
            messagebox.showwarning("Advertencia", "Por favor, complete todos los campos del componente.")

    def cargar_componentes_unitario(self, event):
        selected_item = self.tree_unitarios.focus()
        if selected_item:
            # Limpiar treeview de componentes
            for row in self.tree_componentes.get_children():
                self.tree_componentes.delete(row)

            codigo_unitario = self.tree_unitarios.item(selected_item)["values"][0]

            # Obtener y mostrar los componentes
            componentes = leer_componentes_unitario(codigo_unitario)

            for tipo, items in componentes.items():
                for codigo, desc, unidad, precio, cantidad in items:
                    self.tree_componentes.insert("", "end", values=(tipo.capitalize(), codigo, desc, unidad, f"{precio:.2f}", cantidad))

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()