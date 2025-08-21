<<<<<<< HEAD
# presentacion.py - Versión mejorada y validada para funcionar con crud_db.py
import tkinter as tk
from tkinter import ttk, messagebox
import sys
import mysql.connector
from mysql.connector import errorcode

# Se importa la versión corregida de la base de datos
from crud_db import (
    get_db_connection,
    create_item,
    read_all_apus,
    read_apu_details,
    update_item,
    delete_item,
    calculate_apu_cost,
    add_component_to_apu,
    read_item_by_code
)

class App:
    """Clase principal de la aplicación con la interfaz de usuario."""

    def __init__(self, root):
        """Inicializa la aplicación y la interfaz de usuario."""
        self.root = root
        self.root.title("Análisis de Precios Unitarios")
        self.root.geometry("1100x750")

        # Configuración de los estilos para una apariencia moderna
        style = ttk.Style()
        style.theme_use("clam")  # Utilizar un tema moderno
        style.configure("TNotebook", background="#f0f0f0")
        style.configure("TNotebook.Tab", padding=[15, 7], font=("Arial", 10, "bold"))
        style.configure("TFrame", background="#f8f8f8")
        style.configure("TLabel", background="#f8f8f8", font=("Arial", 10))
        style.configure("TButton", font=("Arial", 10, "bold"), padding=8)
        style.configure("TCombobox", font=("Arial", 10))
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"))
        style.configure("Treeview", font=("Arial", 10), rowheight=25)

        # Notebook para organizar las pestañas
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)

        # Conexión a la base de datos
        self.connection = get_db_connection()
        if not self.connection:
            messagebox.showerror("Error", "No se pudo conectar a la base de datos. La aplicación se cerrará.")
            sys.exit(1)

        # Creación de las pestañas
        self.tab_insumos = ttk.Frame(self.notebook, padding="15")
        self.tab_unitarios = ttk.Frame(self.notebook, padding="15")
        self.notebook.add(self.tab_insumos, text="Gestión de Insumos")
        self.notebook.add(self.tab_unitarios, text="Análisis Unitarios")

        # Bindeo del evento de cambio de pestaña para recargar datos
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_change)

        # Llamada a la creación de la interfaz para cada pestaña
        self.setup_insumos_tab()
        self.setup_unitarios_tab()

        # Al iniciar, cargamos la pestaña de Análisis Unitarios para mostrar datos
        # y luego seleccionamos la pestaña de Insumos para que el usuario pueda empezar.
        self.notebook.select(self.tab_insumos)
        self.cargar_insumos_tabla()
        self.cargar_unitarios_tabla()


    def on_tab_change(self, event):
        """Maneja el evento de cambio de pestaña para recargar datos."""
        current_tab = self.notebook.tab(self.notebook.select(), "text")
        if current_tab == "Gestión de Insumos":
            self.cargar_insumos_tabla()
        elif current_tab == "Análisis Unitarios":
            self.cargar_unitarios_tabla()

    def setup_insumos_tab(self):
        """Configura la interfaz para la pestaña de insumos."""
        # Frame de control de insumos
        control_frame = ttk.Frame(self.tab_insumos, padding="10", relief="groove", borderwidth=2)
        control_frame.pack(fill="x", pady=10)

        # Selección de tabla (Insumo)
        ttk.Label(control_frame, text="Tipo de Insumo:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.insumo_tipo_combo = ttk.Combobox(control_frame, values=['materiales', 'mobra', 'herramienta', 'transporte'], state="readonly")
        self.insumo_tipo_combo.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.insumo_tipo_combo.set('materiales')
        # Se bindea el combobox para que la tabla se recargue automáticamente
        self.insumo_tipo_combo.bind("<<ComboboxSelected>>", self.on_insumo_type_change)

        # Campos de entrada
        ttk.Label(control_frame, text="Código:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.insumo_codigo_entry = ttk.Entry(control_frame)
        self.insumo_codigo_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(control_frame, text="Descripción:").grid(row=1, column=2, padx=5, pady=5, sticky="e")
        self.insumo_descripcion_entry = ttk.Entry(control_frame)
        self.insumo_descripcion_entry.grid(row=1, column=3, padx=5, pady=5, sticky="ew")

        ttk.Label(control_frame, text="Unidad:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.insumo_unidad_entry = ttk.Entry(control_frame)
        self.insumo_unidad_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(control_frame, text="Precio:").grid(row=2, column=2, padx=5, pady=5, sticky="e")
        self.insumo_precio_entry = ttk.Entry(control_frame)
        self.insumo_precio_entry.grid(row=2, column=3, padx=5, pady=5, sticky="ew")

        # Se crean los campos para 'materiales' pero se ocultan al inicio
        self.insumo_peso_label = ttk.Label(control_frame, text="Peso:")
        self.insumo_peso_entry = ttk.Entry(control_frame)

        self.insumo_tipo_material_label = ttk.Label(control_frame, text="Tipo:")
        self.insumo_tipo_material_entry = ttk.Entry(control_frame)

        # Botones de acción
        button_frame = ttk.Frame(control_frame)
        button_frame.grid(row=4, column=0, columnspan=4, pady=10)
        ttk.Button(button_frame, text="Crear", command=self.crear_insumo).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Actualizar", command=self.actualizar_insumo).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Eliminar", command=self.eliminar_insumo).pack(side="left", padx=5)

        # Treeview para mostrar los datos de los insumos
        # Se inicializa con las columnas de 'materiales' por defecto
        columns = ("codigo", "descripcion", "unidad", "precio", "peso", "tipo")
        self.insumos_tree = ttk.Treeview(self.tab_insumos, columns=columns, show="headings")
        self.insumos_tree.pack(expand=True, fill="both")

        for col in columns:
            self.insumos_tree.heading(col, text=col.capitalize())
            self.insumos_tree.column(col, width=100, anchor="center")

        # Bind the selection to load data into entries
        self.insumos_tree.bind("<<TreeviewSelect>>", self.seleccionar_insumo)

        # Llamar al manejador de cambio de tipo para inicializar la UI
        self.on_insumo_type_change()

    def on_insumo_type_change(self, event=None):
        """Ajusta la interfaz de usuario de insumos según el tipo seleccionado."""
        self.limpiar_campos_insumos()
        tabla = self.insumo_tipo_combo.get()

        if tabla == 'materiales':
            # Mostrar los campos de peso y tipo
            self.insumo_peso_label.grid(row=3, column=0, padx=5, pady=5, sticky="e")
            self.insumo_peso_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")
            self.insumo_tipo_material_label.grid(row=3, column=2, padx=5, pady=5, sticky="e")
            self.insumo_tipo_material_entry.grid(row=3, column=3, padx=5, pady=5, sticky="ew")
        else:
            # Ocultar los campos de peso y tipo
            self.insumo_peso_label.grid_forget()
            self.insumo_peso_entry.grid_forget()
            self.insumo_tipo_material_label.grid_forget()
            self.insumo_tipo_material_entry.grid_forget()

        # Recargar la tabla con los datos del nuevo tipo de insumo
        self.cargar_insumos_tabla()

    def setup_unitarios_tab(self):
        """Configura la interfaz para la pestaña de análisis unitarios."""
        # Frame de control principal
        main_frame = ttk.Frame(self.tab_unitarios)
        main_frame.pack(fill="both", expand=True)

        # Frame de unitarios
        unitario_frame = ttk.Frame(main_frame, padding="10", relief="groove", borderwidth=2)
        unitario_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        # Campos de entrada de unitario
        ttk.Label(unitario_frame, text="Código Unitario:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.unitario_codigo_entry = ttk.Entry(unitario_frame)
        self.unitario_codigo_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(unitario_frame, text="Descripción:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.unitario_descripcion_entry = ttk.Entry(unitario_frame)
        self.unitario_descripcion_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(unitario_frame, text="Unidad:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.unitario_unidad_entry = ttk.Entry(unitario_frame)
        self.unitario_unidad_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        # Botones de acción para unitario
        button_frame = ttk.Frame(unitario_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=10)
        ttk.Button(button_frame, text="Crear Unitario", command=self.crear_unitario).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Eliminar Unitario", command=self.eliminar_unitario).pack(side="left", padx=5)

        # Treeview para mostrar los unitarios
        unitarios_tree_columns = ("codigo", "descripcion", "unidad")
        self.unitarios_tree = ttk.Treeview(unitario_frame, columns=unitarios_tree_columns, show="headings")
        self.unitarios_tree.grid(row=4, column=0, columnspan=2, sticky="nsew")

        for col in unitarios_tree_columns:
            self.unitarios_tree.heading(col, text=col.capitalize())
            self.unitarios_tree.column(col, width=150, anchor="center")

        self.unitarios_tree.bind("<<TreeviewSelect>>", self.seleccionar_unitario)

        # Frame de componentes
        componentes_frame = ttk.Frame(main_frame, padding="10", relief="groove", borderwidth=2)
        componentes_frame.pack(side="right", fill="both", expand=True, padx=5, pady=5)

        ttk.Label(componentes_frame, text="Componentes del Unitario", font=("Arial", 12, "bold")).pack(pady=5)

        # Etiqueta para el costo total
        self.costo_total_label = ttk.Label(componentes_frame, text="Costo Total: $0.00", font=("Arial", 12, "bold"))
        self.costo_total_label.pack(pady=5)

        # Treeview para mostrar los componentes
        # Se agrega la nueva columna 'costo'
        componentes_tree_columns = ("tipo", "codigo", "descripcion", "unidad", "precio", "cantidad", "costo")
        self.componentes_tree = ttk.Treeview(componentes_frame, columns=componentes_tree_columns, show="headings")
        self.componentes_tree.pack(fill="both", expand=True)

        for col in componentes_tree_columns:
            self.componentes_tree.heading(col, text=col.capitalize())
            self.componentes_tree.column(col, width=100, anchor="center")

        # Sección para agregar componentes
        add_comp_frame = ttk.Frame(componentes_frame, padding=5, relief="ridge", borderwidth=1)
        add_comp_frame.pack(fill="x", pady=10)

        ttk.Label(add_comp_frame, text="Añadir Componente", font=("Arial", 10, "bold")).grid(row=0, column=0, columnspan=2)

        ttk.Label(add_comp_frame, text="Tipo:").grid(row=1, column=0, padx=5, pady=2, sticky="e")
        self.comp_tipo_combo = ttk.Combobox(add_comp_frame, values=['materiales', 'mobra', 'herramienta', 'transporte'], state="readonly")
        self.comp_tipo_combo.grid(row=1, column=1, padx=5, pady=2, sticky="ew")
        self.comp_tipo_combo.set('materiales')

        ttk.Label(add_comp_frame, text="Código:").grid(row=2, column=0, padx=5, pady=2, sticky="e")
        self.comp_codigo_entry = ttk.Entry(add_comp_frame)
        self.comp_codigo_entry.grid(row=2, column=1, padx=5, pady=2, sticky="ew")
        # Se añade un bindeo para actualizar la descripción
        self.comp_codigo_entry.bind("<FocusOut>", self.obtener_descripcion_insumo)
        self.comp_codigo_entry.bind("<Return>", self.obtener_descripcion_insumo)

        ttk.Label(add_comp_frame, text="Descripción:").grid(row=3, column=0, padx=5, pady=2, sticky="e")
        self.comp_descripcion_label = ttk.Label(add_comp_frame, text="", wraplength=200, justify="left")
        self.comp_descripcion_label.grid(row=3, column=1, padx=5, pady=2, sticky="ew")

        ttk.Label(add_comp_frame, text="Unidad:").grid(row=4, column=0, padx=5, pady=2, sticky="e")
        self.comp_unidad_label = ttk.Label(add_comp_frame, text="", wraplength=50, justify="left")
        self.comp_unidad_label.grid(row=4, column=1, padx=5, pady=2, sticky="ew")

        ttk.Label(add_comp_frame, text="Cantidad:").grid(row=5, column=0, padx=5, pady=2, sticky="e")
        self.comp_cantidad_entry = ttk.Entry(add_comp_frame)
        self.comp_cantidad_entry.grid(row=5, column=1, padx=5, pady=2, sticky="ew")

        ttk.Button(add_comp_frame, text="Añadir al Unitario", command=self.agregar_componente_a_apu).grid(row=6, column=0, columnspan=2, pady=5)

    def cargar_insumos_tabla(self, event=None):
        """Carga los datos de los insumos en el Treeview."""
        tabla = self.insumo_tipo_combo.get()
        # Limpiar la tabla de insumos
        for i in self.insumos_tree.get_children():
            self.insumos_tree.delete(i)

        # Definir las columnas dinámicamente
        if tabla == 'materiales':
            columns = ("codigo", "descripcion", "unidad", "precio", "peso", "tipo")
        else:
            columns = ("codigo", "descripcion", "unidad", "precio")

        # Actualizar las columnas del Treeview
        self.insumos_tree['columns'] = columns
        for col in columns:
            self.insumos_tree.heading(col, text=col.capitalize())
            self.insumos_tree.column(col, width=100, anchor="center")

        cursor = self.connection.cursor(dictionary=True)
        try:
            query = f"SELECT {', '.join(columns)} FROM {tabla}"
            cursor.execute(query)
            insumos = cursor.fetchall()
            if insumos:
                for insumo in insumos:
                    # Usar una tupla de los valores para insertar en el Treeview
                    values = tuple(insumo.get(c) for c in columns)
                    self.insumos_tree.insert("", "end", values=values)
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al leer insumos de la tabla '{tabla}': {err}")
        finally:
            cursor.close()

    def seleccionar_insumo(self, event):
        """Carga los datos del insumo seleccionado en los campos de entrada."""
        selected_item = self.insumos_tree.focus()
        if not selected_item:
            return

        values = self.insumos_tree.item(selected_item, "values")
        self.limpiar_campos_insumos()

        # Manejar las columnas opcionales para 'materiales' de forma más robusta
        try:
            self.insumo_codigo_entry.insert(0, values[0])
            self.insumo_descripcion_entry.insert(0, values[1])
            self.insumo_unidad_entry.insert(0, values[2])
            self.insumo_precio_entry.insert(0, values[3])

            if len(values) > 4:
                self.insumo_peso_entry.insert(0, values[4] if values[4] is not None else "")
            if len(values) > 5:
                self.insumo_tipo_material_entry.insert(0, values[5] if values[5] is not None else "")
        except IndexError:
            # Esto maneja el caso donde las columnas de la tabla son menos de lo esperado.
            pass

    def crear_insumo(self):
        """Crea un nuevo insumo en la base de datos."""
        tabla = self.insumo_tipo_combo.get()
        codigo = self.insumo_codigo_entry.get()
        descripcion = self.insumo_descripcion_entry.get()
        unidad = self.insumo_unidad_entry.get()
        precio_str = self.insumo_precio_entry.get()

        if not all([codigo, descripcion, unidad, precio_str]):
            messagebox.showerror("Error", "Los campos Código, Descripción, Unidad y Precio son obligatorios.")
            return

        try:
            precio = float(precio_str)
            data = {
                "codigo": codigo,
                "descripcion": descripcion,
                "unidad": unidad,
                "precio": precio
            }
            if tabla == 'materiales':
                peso_str = self.insumo_peso_entry.get()
                tipo = self.insumo_tipo_material_entry.get()
                peso = float(peso_str) if peso_str else None
                data["peso"] = peso
                data["tipo"] = tipo if tipo else None

            create_item(self.connection, tabla, data)
            messagebox.showinfo("Éxito", "Insumo creado correctamente.")
            self.limpiar_campos_insumos()
            self.cargar_insumos_tabla()
        except ValueError:
            messagebox.showerror("Error", "El precio y el peso deben ser números válidos.")
        except mysql.connector.Error as e:
            messagebox.showerror("Error de Base de Datos", f"No se pudo crear el insumo: {e}")

    def actualizar_insumo(self):
        """Actualiza un insumo existente."""
        tabla = self.insumo_tipo_combo.get()
        codigo = self.insumo_codigo_entry.get()

        if not codigo:
            messagebox.showerror("Error", "Debe seleccionar un insumo para actualizar.")
            return

        try:
            precio = float(self.insumo_precio_entry.get())
            data = {
                "descripcion": self.insumo_descripcion_entry.get(),
                "unidad": self.insumo_unidad_entry.get(),
                "precio": precio
            }
            if tabla == 'materiales':
                peso_str = self.insumo_peso_entry.get()
                tipo = self.insumo_tipo_material_entry.get()
                peso = float(peso_str) if peso_str else None
                data["peso"] = peso
                data["tipo"] = tipo if tipo else None

            condition = {"codigo": codigo}
            update_item(self.connection, tabla, data, condition)
            messagebox.showinfo("Éxito", "Insumo actualizado correctamente.")
            self.limpiar_campos_insumos()
            self.cargar_insumos_tabla()
        except ValueError:
            messagebox.showerror("Error", "El precio y el peso deben ser números válidos.")
        except mysql.connector.Error as e:
            messagebox.showerror("Error de Base de Datos", f"No se pudo actualizar el insumo: {e}")

    def eliminar_insumo(self):
        """Elimina un insumo."""
        tabla = self.insumo_tipo_combo.get()
        codigo = self.insumo_codigo_entry.get()

        if not codigo:
            messagebox.showerror("Error", "Debe seleccionar un insumo para eliminar.")
            return

        if messagebox.askyesno("Confirmar Eliminación", f"¿Está seguro de que desea eliminar el insumo con código {codigo}?"):
            try:
                condition = {"codigo": codigo}
                delete_item(self.connection, tabla, condition)
                messagebox.showinfo("Éxito", "Insumo eliminado correctamente.")
                self.limpiar_campos_insumos()
                self.cargar_insumos_tabla()
            except mysql.connector.Error as e:
                messagebox.showerror("Error de Base de Datos", f"No se pudo eliminar el insumo: {e}")

    def limpiar_campos_insumos(self):
        """Limpia los campos de entrada de la pestaña de insumos."""
        self.insumo_codigo_entry.delete(0, tk.END)
        self.insumo_descripcion_entry.delete(0, tk.END)
        self.insumo_unidad_entry.delete(0, tk.END)
        self.insumo_precio_entry.delete(0, tk.END)
        self.insumo_peso_entry.delete(0, tk.END)
        self.insumo_tipo_material_entry.delete(0, tk.END)

    def cargar_unitarios_tabla(self):
        """Carga los análisis unitarios en el Treeview."""
        # Limpiar la tabla antes de cargar
        for i in self.unitarios_tree.get_children():
            self.unitarios_tree.delete(i)

        unitarios = read_all_apus(self.connection)
        if unitarios:
            for unitario in unitarios:
                self.unitarios_tree.insert("", "end", values=(unitario['codigo'], unitario['descripcion'], unitario['unidad']))

    def seleccionar_unitario_por_codigo(self, codigo):
        """Busca y selecciona un análisis unitario por su código."""
        for item in self.unitarios_tree.get_children():
            if self.unitarios_tree.item(item, 'values')[0] == codigo:
                self.unitarios_tree.selection_set(item)
                self.unitarios_tree.focus(item)
                return True
        return False

    def seleccionar_unitario(self, event):
        """
        Carga los datos del unitario seleccionado en los campos de entrada
        y los componentes asociados en el Treeview de componentes.
        """
        self.limpiar_campos_componentes()
        selected_item = self.unitarios_tree.focus()
        if not selected_item:
            return

        values = self.unitarios_tree.item(selected_item, "values")
        codigo_unitario = values[0]

        # Limpiar y rellenar los campos de entrada de APU
        self.unitario_codigo_entry.delete(0, tk.END)
        self.unitario_descripcion_entry.delete(0, tk.END)
        self.unitario_unidad_entry.delete(0, tk.END)

        self.unitario_codigo_entry.insert(0, values[0])
        self.unitario_descripcion_entry.insert(0, values[1])
        self.unitario_unidad_entry.insert(0, values[2])

        # Cargar los componentes del unitario seleccionado
        self.cargar_componentes_unitario(codigo_unitario)

        # Calcular y mostrar el costo total
        costo_total = calculate_apu_cost(self.connection, codigo_unitario)
        self.costo_total_label.config(text=f"Costo Total: ${costo_total:.2f}")

    def crear_unitario(self):
        """Crea un nuevo análisis unitario en la base de datos."""
        codigo = self.unitario_codigo_entry.get()
        descripcion = self.unitario_descripcion_entry.get()
        unidad = self.unitario_unidad_entry.get()

        if not all([codigo, descripcion, unidad]):
            messagebox.showerror("Error", "Todos los campos de Análisis Unitario son obligatorios.")
            return

        try:
            data = {
                "codigo": codigo,
                "descripcion": descripcion,
                "unidad": unidad
            }
            create_item(self.connection, 'unitario', data)
            messagebox.showinfo("Éxito", "Análisis Unitario creado correctamente.")
            self.limpiar_campos_unitarios()
            self.cargar_unitarios_tabla() 
            self.seleccionar_unitario_por_codigo(codigo)
        except mysql.connector.Error as e:
            messagebox.showerror("Error de Base de Datos", f"No se pudo crear el Análisis Unitario: {e}")

    def eliminar_unitario(self):
        """Elimina un análisis unitario."""
        codigo = self.unitario_codigo_entry.get()
        if not codigo:
            messagebox.showerror("Error", "Debe seleccionar un APU para eliminar.")
            return

        if messagebox.askyesno("Confirmar Eliminación", f"¿Está seguro de que desea eliminar el APU con código {codigo}?"):
            try:
                condition = {"codigo": codigo}
                delete_item(self.connection, 'unitario', condition)
                messagebox.showinfo("Éxito", "APU eliminado correctamente.")
                self.limpiar_campos_unitarios()
                self.limpiar_campos_componentes()
                self.costo_total_label.config(text="Costo Total: $0.00")
                self.cargar_unitarios_tabla()
            except mysql.connector.Error as e:
                messagebox.showerror("Error de Base de Datos", f"No se pudo eliminar el APU: {e}")

    def limpiar_campos_unitarios(self):
        """Limpia los campos de entrada de la pestaña de unitarios."""
        self.unitario_codigo_entry.delete(0, tk.END)
        self.unitario_descripcion_entry.delete(0, tk.END)
        self.unitario_unidad_entry.delete(0, tk.END)

    def limpiar_campos_componentes(self):
        """Limpia el Treeview de componentes."""
        for item in self.componentes_tree.get_children():
            self.componentes_tree.delete(item)

    def cargar_componentes_unitario(self, codigo_unitario):
        """Carga los componentes del unitario seleccionado en el Treeview."""
        self.limpiar_campos_componentes()

        details = read_apu_details(self.connection, codigo_unitario)

        if details and details['components']:
            for comp_type, components in details['components'].items():
                if components:
                    for comp in components:
                        # Se inserta la nueva columna de costo
                        self.componentes_tree.insert("", "end", values=(
                            comp['tipo'],
                            comp['codigo'],
                            comp['descripcion'],
                            comp['unidad'],
                            f"${comp['precio']:.2f}",
                            comp['cantidad'],
                            f"${comp['costo_componente']:.2f}"
                        ))

    def obtener_descripcion_insumo(self, event=None):
        """Busca y muestra la descripción y la unidad del insumo en los labels de componentes."""
        tipo_componente = self.comp_tipo_combo.get()
        codigo_componente = self.comp_codigo_entry.get()

        self.comp_descripcion_label.config(text="")
        self.comp_unidad_label.config(text="")

        if not codigo_componente:
            return

        insumo = read_item_by_code(self.connection, tipo_componente, codigo_componente)

        if insumo:
            self.comp_descripcion_label.config(text=insumo['descripcion'])
            self.comp_unidad_label.config(text=insumo['unidad'])
        else:
            self.comp_descripcion_label.config(text="Insumo no encontrado.")
            self.comp_unidad_label.config(text="")

    def agregar_componente_a_apu(self):
        """Añade un componente a un Análisis Unitario (AU) seleccionado."""
        selected_item = self.unitarios_tree.focus()
        if not selected_item:
            messagebox.showerror("Error", "Debes seleccionar un Análisis Unitario de la lista primero.")
            return

        codigo_unitario = self.unitarios_tree.item(selected_item, "values")[0]

        tipo_componente = self.comp_tipo_combo.get()
        codigo_componente = self.comp_codigo_entry.get()
        cantidad = self.comp_cantidad_entry.get()

        if not all([tipo_componente, codigo_componente, cantidad]):
            messagebox.showerror("Error", "Debes llenar todos los campos del componente (Tipo, Código, Cantidad).")
            return

        try:
            cantidad = float(cantidad)

            add_component_to_apu(self.connection, codigo_unitario, tipo_componente, codigo_componente, cantidad)
            messagebox.showinfo("Éxito", "Componente añadido correctamente.")

            self.comp_codigo_entry.delete(0, tk.END)
            self.comp_cantidad_entry.delete(0, tk.END)
            self.comp_descripcion_label.config(text="")
            self.comp_unidad_label.config(text="")

            self.cargar_componentes_unitario(codigo_unitario)
            costo_total = calculate_apu_cost(self.connection, codigo_unitario)
            self.costo_total_label.config(text=f"Costo Total: ${costo_total:.2f}")

        except ValueError:
            messagebox.showerror("Error", "La cantidad debe ser un número.")
        except mysql.connector.Error as e:
            messagebox.showerror("Error de Base de Datos", f"No se pudo añadir el componente: {e}")
=======
# presentacion.py
import tkinter as tk
from tkinter import ttk, messagebox

# Se asume que este módulo existe y contiene las funciones necesarias
# NOTA: Deberás implementar las funciones 'eliminar_' en crud_db.py
from crud_db import (
    crear_material, leer_materiales, actualizar_material,
    crear_mobra, leer_mobra, actualizar_mobra,
    crear_herramienta, leer_herramientas, actualizar_herramienta,
    crear_transporte, leer_transporte, actualizar_transporte,
    crear_unitario, leer_unitarios, crear_componente_unitario, leer_componentes_unitario,
    crear_tablas
)

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestor de Presupuestos")
        self.root.geometry("1000x700")

        # Llamar a crear_tablas para asegurar que la DB está lista
        crear_tablas()

        # Crear el NoteBook para las pestañas
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(pady=10, expand=True, fill="both")

        # Configuración de los datos para cada pestaña CRUDS (Materiales, Mobra, etc.)
        self.tabs_data = {
            "Materiales": {
                "frame": ttk.Frame(self.notebook),
                "fields": ["Código", "Descripción", "Unidad", "Precio", "Peso", "Tipo"],
                "crud_funcs": {
                    "create": crear_material,
                    "read": leer_materiales,
                    "update": actualizar_material,
                    "delete": None  # Deberás implementar esta función en crud_db.py
                }
            },
            "Mano de Obra": {
                "frame": ttk.Frame(self.notebook),
                "fields": ["Código", "Descripción", "Unidad", "Precio"],
                "crud_funcs": {
                    "create": crear_mobra,
                    "read": leer_mobra,
                    "update": actualizar_mobra,
                    "delete": None
                }
            },
            "Herramientas": {
                "frame": ttk.Frame(self.notebook),
                "fields": ["Código", "Descripción", "Unidad", "Precio"],
                "crud_funcs": {
                    "create": crear_herramienta,
                    "read": leer_herramientas,
                    "update": actualizar_herramienta,
                    "delete": None
                }
            },
            "Transporte": {
                "frame": ttk.Frame(self.notebook),
                "fields": ["Código", "Descripción", "Unidad", "Precio"],
                "crud_funcs": {
                    "create": crear_transporte,
                    "read": leer_transporte,
                    "update": actualizar_transporte,
                    "delete": None
                }
            }
        }

        # Crear y configurar pestañas de forma genérica
        for name, data in self.tabs_data.items():
            self.notebook.add(data["frame"], text=name)
            self.setup_crud_tab(
                data["frame"],
                name,
                data["fields"],
                data["crud_funcs"]
            )

        # Configurar la pestaña de Análisis Unitario por separado
        self.tab_unitarios = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_unitarios, text="Análisis Unitario")
        self.setup_unitarios_tab()

    # ====================================================================
    # --- Métodos Genéricos para Pestañas CRUD ---
    # ====================================================================

    def setup_crud_tab(self, tab, title, fields, crud_funcs):
        # Frame para la entrada de datos (arriba)
        frame_input = ttk.LabelFrame(tab, text=f"Crear/Actualizar {title}")
        frame_input.pack(padx=10, pady=10, fill="x")

        # Almacena los entries para este tab
        entries = {}
        for i, field in enumerate(fields):
            label = ttk.Label(frame_input, text=f"{field}:")
            label.grid(row=i, column=0, padx=5, pady=2, sticky="e")
            entry = ttk.Entry(frame_input)
            entry.grid(row=i, column=1, padx=5, pady=2, sticky="we")
            entries[field] = entry
        
        frame_input.columnconfigure(1, weight=1)

        # Botones
        frame_buttons = ttk.Frame(frame_input)
        frame_buttons.grid(row=len(fields), column=0, columnspan=2, pady=10)
        
        btn_crear = ttk.Button(frame_buttons, text="Crear", command=lambda: self.crear_generico(
            crud_funcs["create"], entries, self.actualizar_treeview_generico, title, fields, tab))
        btn_crear.pack(side="left", padx=5)
        
        btn_actualizar = ttk.Button(frame_buttons, text="Actualizar", command=lambda: self.actualizar_generico(
            crud_funcs["update"], entries, self.actualizar_treeview_generico, title, fields, tab))
        btn_actualizar.pack(side="left", padx=5)
        
        btn_eliminar = ttk.Button(frame_buttons, text="Eliminar", command=lambda: self.eliminar_generico(
            crud_funcs["delete"], self.actualizar_treeview_generico, title, tab))
        btn_eliminar.pack(side="left", padx=5)
        
        # Separador
        ttk.Separator(tab, orient="horizontal").pack(fill="x", pady=10)
        
        # Treeview para mostrar los datos
        tree = ttk.Treeview(tab, columns=fields, show="headings")
        tree.pack(padx=10, pady=10, expand=True, fill="both")
        
        for field in fields:
            tree.heading(field, text=field)
            tree.column(field, width=100)
            
        tree.bind("<<TreeviewSelect>>", lambda event: self.cargar_generico(event, entries, tree))
        
        # Asociar Treeview y entries a la clase para acceso
        setattr(self, f'entries_{title.lower().replace(" ", "")}', entries)
        setattr(self, f'tree_{title.lower().replace(" ", "")}', tree)
        
        # Cargar datos al iniciar la pestaña
        self.actualizar_treeview_generico(crud_funcs["read"], tree, fields)

    def actualizar_treeview_generico(self, read_func, tree, fields):
        # Borrar datos existentes
        for row in tree.get_children():
            tree.delete(row)
        
        # Insertar nuevos datos
        data = read_func()
        for item in data:
            tree.insert("", "end", values=item)

    def crear_generico(self, create_func, entries, update_func, title, fields, tab):
        try:
            values = [entries[field].get() for field in fields]
            
            # Validar campos no numéricos
            if not all(values):
                 messagebox.showwarning("Advertencia", "Todos los campos deben estar llenos.")
                 return
            
            # Manejo de campos numéricos (asume que los últimos 2 campos son numéricos si existen)
            num_values = []
            if len(values) > 3: # Asume que "Precio" y "Peso" son los últimos
                try:
                    num_values = [float(values[3]), float(values[4])]
                    values = values[:3] + num_values + values[5:]
                except (ValueError, IndexError):
                    messagebox.showerror("Error", "Los campos 'Precio' y 'Peso' deben ser números.")
                    return
            
            create_func(*values)
            update_func(self.tabs_data[title]["crud_funcs"]["read"], getattr(self, f'tree_{title.lower().replace(" ", "")}'), fields)
            messagebox.showinfo("Éxito", f"{title} creado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")

    def actualizar_generico(self, update_func, entries, update_func_tree, title, fields, tab):
        tree = getattr(self, f'tree_{title.lower().replace(" ", "")}')
        selected_item = tree.focus()
        if not selected_item:
            messagebox.showwarning("Advertencia", f"Por favor, seleccione un(a) {title.lower()} para actualizar.")
            return

        try:
            codigo = tree.item(selected_item)["values"][0]
            values = [entries[field].get() for field in fields[1:]] # No incluir el código
            
            # Validar campos no numéricos
            if not all(values):
                 messagebox.showwarning("Advertencia", "Todos los campos deben estar llenos.")
                 return

            # Manejo de campos numéricos
            num_values = []
            if len(values) > 2:
                try:
                    num_values = [float(values[2]), float(values[3])]
                    values = values[:2] + num_values + values[4:]
                except (ValueError, IndexError):
                    messagebox.showerror("Error", "Los campos 'Precio' y 'Peso' deben ser números.")
                    return
            
            update_func(codigo, *values)
            update_func_tree(self.tabs_data[title]["crud_funcs"]["read"], tree, fields)
            messagebox.showinfo("Éxito", f"{title} actualizado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")

    def eliminar_generico(self, delete_func, update_func_tree, title, tab):
        tree = getattr(self, f'tree_{title.lower().replace(" ", "")}')
        selected_item = tree.focus()
        if not selected_item:
            messagebox.showwarning("Advertencia", f"Por favor, seleccione un(a) {title.lower()} para eliminar.")
            return

        codigo = tree.item(selected_item)["values"][0]
        if delete_func:
            try:
                # delete_func(codigo) # La llamada sería así
                print(f"Llamando a la función de eliminación para {title} con código: {codigo}")
                messagebox.showinfo("Éxito", f"{title} con código {codigo} eliminado correctamente (simulado).")
                # update_func_tree(...) # Descomentar esto y la línea anterior para actualizar el treeview
            except Exception as e:
                messagebox.showerror("Error", f"Error al eliminar {title}: {e}")
        else:
            messagebox.showerror("Error", "Función de eliminación no implementada.")


    def cargar_generico(self, event, entries, tree):
        selected_item = tree.focus()
        if selected_item:
            values = tree.item(selected_item)["values"]
            fields = list(entries.keys())
            for i, field in enumerate(fields):
                entries[field].delete(0, tk.END)
                entries[field].insert(0, values[i])

    # ====================================================================
    # --- Configuración de Pestaña de Análisis Unitario (específica) ---
    # ====================================================================
    def setup_unitarios_tab(self):
        # Frame de la izquierda para crear/seleccionar unitarios
        frame_left = ttk.Frame(self.tab_unitarios)
        frame_left.pack(side="left", padx=10, pady=10, fill="y", expand=False)

        # Frame de la derecha para gestionar componentes
        frame_right = ttk.Frame(self.tab_unitarios)
        frame_right.pack(side="right", padx=10, pady=10, fill="both", expand=True)

        # Sección para crear un nuevo unitario
        frame_crear_unitario = ttk.LabelFrame(frame_left, text="Crear Nuevo Análisis Unitario")
        frame_crear_unitario.pack(pady=10, fill="x")

        ttk.Label(frame_crear_unitario, text="Código:").grid(row=0, column=0, padx=5, pady=2, sticky="w")
        self.entry_unitario_codigo = ttk.Entry(frame_crear_unitario)
        self.entry_unitario_codigo.grid(row=0, column=1, padx=5, pady=2, sticky="we")

        ttk.Label(frame_crear_unitario, text="Descripción:").grid(row=1, column=0, padx=5, pady=2, sticky="w")
        self.entry_unitario_desc = ttk.Entry(frame_crear_unitario)
        self.entry_unitario_desc.grid(row=1, column=1, padx=5, pady=2, sticky="we")

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

        # Combobox para seleccionar tipo de componente
        ttk.Label(self.frame_componentes, text="Tipo:").grid(row=0, column=0, padx=5, pady=2, sticky="w")
        self.component_type_var = tk.StringVar()
        self.component_type_combo = ttk.Combobox(self.frame_componentes, textvariable=self.component_type_var,
                                                 values=["material", "mobra", "herramienta", "transporte"])
        self.component_type_combo.grid(row=0, column=1, padx=5, pady=2, sticky="we")
        self.component_type_combo.bind("<<ComboboxSelected>>", self.actualizar_componentes_combo)
        
        # Combobox para seleccionar el componente
        ttk.Label(self.frame_componentes, text="Código:").grid(row=1, column=0, padx=5, pady=2, sticky="w")
        self.component_combo_var = tk.StringVar()
        self.component_combo = ttk.Combobox(self.frame_componentes, textvariable=self.component_combo_var)
        self.component_combo.grid(row=1, column=1, padx=5, pady=2, sticky="we")

        # Entrada para la cantidad
        ttk.Label(self.frame_componentes, text="Cantidad:").grid(row=2, column=0, padx=5, pady=2, sticky="w")
        self.entry_cantidad_componente = ttk.Entry(self.frame_componentes)
        self.entry_cantidad_componente.grid(row=2, column=1, padx=5, pady=2, sticky="we")

        # Botones de componentes
        frame_comp_buttons = ttk.Frame(self.frame_componentes)
        frame_comp_buttons.grid(row=3, column=0, columnspan=2, pady=10, sticky="ew")
        
        btn_add_componente = ttk.Button(frame_comp_buttons, text="Añadir Componente", command=self.agregar_componente_a_unitario)
        btn_add_componente.pack(side="left", padx=5, fill="x", expand=True)

        btn_del_componente = ttk.Button(frame_comp_buttons, text="Eliminar Componente", command=self.eliminar_componente_unitario)
        btn_del_componente.pack(side="left", padx=5, fill="x", expand=True)
        
        # Treeview para mostrar los componentes del unitario
        self.tree_componentes = ttk.Treeview(self.frame_componentes, columns=("Tipo", "Código", "Descripción", "Unidad", "Precio", "Cantidad", "Subtotal"), show="headings")
        self.tree_componentes.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
        self.tree_componentes.grid_rowconfigure(4, weight=1)
        
        headings = {"Tipo": 80, "Código": 80, "Descripción": 200, "Unidad": 60, "Precio": 60, "Cantidad": 60, "Subtotal": 70}
        for col, width in headings.items():
            self.tree_componentes.heading(col, text=col)
            self.tree_componentes.column(col, width=width)
        
        # Etiqueta para el total
        self.label_total_unitario = ttk.Label(self.frame_componentes, text="Costo Total: $0.00", font=("Helvetica", 12, "bold"))
        self.label_total_unitario.grid(row=5, column=0, columnspan=2, pady=10, sticky="e")

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
        selected_item = self.tree_unitarios.focus() 
        if not selected_item:
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

    def eliminar_componente_unitario(self):
        selected_item_unitario = self.tree_unitarios.focus()
        selected_item_componente = self.tree_componentes.focus()
        
        if not selected_item_unitario or not selected_item_componente:
            messagebox.showwarning("Advertencia", "Por favor, seleccione un análisis unitario y un componente para eliminar.")
            return

        codigo_unitario = self.tree_unitarios.item(selected_item_unitario)["values"][0]
        componente_values = self.tree_componentes.item(selected_item_componente)["values"]
        tipo_componente = componente_values[0].lower()
        codigo_componente = componente_values[1]

        # Llama a la función de eliminación (que debes implementar en crud_db.py)
        # delete_componente_unitario(codigo_unitario, tipo_componente, codigo_componente)
        
        # Simula la eliminación
        self.tree_componentes.delete(selected_item_componente)
        messagebox.showinfo("Éxito", "Componente eliminado correctamente.")
        self.calcular_total_unitario()

    def cargar_componentes_unitario(self, event):
        selected_item = self.tree_unitarios.focus()
        if selected_item:
            for row in self.tree_componentes.get_children():
                self.tree_componentes.delete(row)

            codigo_unitario = self.tree_unitarios.item(selected_item)["values"][0]
            componentes = leer_componentes_unitario(codigo_unitario)
            
            for tipo, items in componentes.items():
                for codigo, desc, unidad, precio, cantidad in items:
                    subtotal = precio * cantidad
                    self.tree_componentes.insert("", "end", values=(tipo.capitalize(), codigo, desc, unidad, f"{precio:.2f}", cantidad, f"{subtotal:.2f}"))
            
            self.calcular_total_unitario()

    def calcular_total_unitario(self):
        total = 0.0
        for item in self.tree_componentes.get_children():
            values = self.tree_componentes.item(item)["values"]
            subtotal = float(values[6])
            total += subtotal
        
        self.label_total_unitario.config(text=f"Costo Total: ${total:.2f}")
>>>>>>> 6b069589aa7a2efcb39fa2a7e4de5280ce0ddfce

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
<<<<<<< HEAD
    root.mainloop()
=======
    root.mainloop()  
>>>>>>> 6b069589aa7a2efcb39fa2a7e4de5280ce0ddfce
