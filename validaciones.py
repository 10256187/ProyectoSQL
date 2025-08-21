import mysql.connector
from mysql.connector import errorcode, Error
from tkinter import Tk, Label, Entry, Button, Scrollbar, Listbox, messagebox, END
from tkinter.ttk import Notebook, Treeview, Frame, Style, Combobox
import sys

# --- 1. Configuración de la conexión a la base de datos ---
DB_CONFIG = {
    'user': 'root',
    'password': '123@Chepe$#', 
    'host': 'localhost',
    'database': 'ProyectoSQL'
}

# --- 2. Funciones para interactuar con la base de datos ---
def get_connection():
    """Establece y devuelve una conexión a la base de datos."""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        messagebox.showerror("Error de Conexión", f"Error al conectar a la base de datos: {e}")
        return None

def insert_data(table_name, data):
    """
    Inserta una nueva fila de datos en la tabla especificada.
    data debe ser un diccionario con los nombres de las columnas y sus valores.
    """
    connection = get_connection()
    if connection is None:
        return
    
    try:
        cursor = connection.cursor()
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['%s'] * len(data))
        sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        cursor.execute(sql, list(data.values()))
        connection.commit()
        messagebox.showinfo("Éxito", "Datos insertados correctamente.")
        return True
    except Error as e:
        messagebox.showerror("Error", f"Error al insertar datos: {e}")
        return False
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def update_data(table_name, data, where_clause):
    """
    Actualiza una fila de datos en la tabla especificada.
    where_clause debe ser un diccionario con la columna y el valor para identificar la fila.
    """
    connection = get_connection()
    if connection is None:
        return
    
    try:
        cursor = connection.cursor()
        set_clause = ', '.join([f"{key} = %s" for key in data.keys()])
        where_key = list(where_clause.keys())[0]
        sql = f"UPDATE {table_name} SET {set_clause} WHERE {where_key} = %s"
        values = list(data.values()) + [list(where_clause.values())[0]]
        cursor.execute(sql, values)
        connection.commit()
        messagebox.showinfo("Éxito", "Datos actualizados correctamente.")
        return True
    except Error as e:
        messagebox.showerror("Error", f"Error al actualizar datos: {e}")
        return False
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def delete_data(table_name, where_clause):
    """
    Elimina una fila de datos de la tabla especificada.
    where_clause debe ser un diccionario con la columna y el valor para identificar la fila.
    """
    connection = get_connection()
    if connection is None:
        return
    
    try:
        cursor = connection.cursor()
        where_key = list(where_clause.keys())[0]
        sql = f"DELETE FROM {table_name} WHERE {where_key} = %s"
        cursor.execute(sql, (list(where_clause.values())[0],))
        connection.commit()
        messagebox.showinfo("Éxito", "Datos eliminados correctamente.")
        return True
    except Error as e:
        messagebox.showerror("Error", f"Error al eliminar datos: {e}")
        return False
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def get_all_data(table_name):
    """Devuelve todos los datos de la tabla especificada."""
    connection = get_connection()
    if connection is None:
        return []
    
    try:
        cursor = connection.cursor(dictionary=True) # Devuelve resultados como diccionarios
        sql = f"SELECT * FROM {table_name}"
        cursor.execute(sql)
        return cursor.fetchall()
    except Error as e:
        messagebox.showerror("Error", f"Error al obtener datos: {e}")
        return []
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# --- 3. Lógica de la interfaz gráfica (tkinter) ---
class ProjectApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Datos - ProyectoSQL")
        self.root.geometry("1000x800")
        
        # Agregamos un estilo para la Treeview
        style = Style()
        style.configure("Treeview.Heading", font=('Helvetica', 10, 'bold'))

        # Crear un contenedor de pestañas (Notebook)
        self.notebook = Notebook(root)
        self.notebook.pack(pady=10, expand=True, fill="both")

        # Crear pestañas para cada tabla
        self.tables = ['materiales', 'mobra', 'herramienta', 'transporte']
        self.frames = {}
        self.entry_fields = {}
        self.treeviews = {}
        self.selected_item = None
        
        # Diccionarios para los valores de las listas desplegables
        self.valid_units = ['UN', 'ML', 'KM', 'LB', 'KG', 'TN', 'SC', 'GL', 'GB', 'PG', 'M2', 'M3', 'Lt']
        self.valid_types = ['MAR', 'HIE', 'CEM', 'CON', 'HER', 'CAB', 'ESM', 'ESC', 'ELE', 'ILU', 'CPM', 'CAP']

        for table in self.tables:
            frame = Frame(self.notebook, padding=10)
            self.frames[table] = frame
            self.notebook.add(frame, text=table.capitalize())
            self.setup_ui_for_table(frame, table)
        
        # Conectar el evento de cambio de pestaña para recargar los datos
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_changed)
    
    def on_tab_changed(self, event):
        """Maneja el evento de cambio de pestaña para recargar los datos."""
        selected_tab = event.widget.tab(event.widget.select(), "text").lower()
        self.refresh_treeview(selected_tab)

    def setup_ui_for_table(self, parent_frame, table_name):
        """Configura la interfaz de usuario para una tabla específica."""
        if table_name == 'materiales':
            self.setup_materiales_ui(parent_frame, table_name)
        else:
            self.setup_generic_ui(parent_frame, table_name)
            
    def setup_materiales_ui(self, parent_frame, table_name):
        """Configura la interfaz para la tabla de materiales."""
        form_frame = Frame(parent_frame, padding=10)
        form_frame.pack(fill="x", pady=5)
        
        # Campos de entrada
        field_names = ['codigo', 'descripcion', 'unidad', 'precio', 'peso', 'tipo']
        self.entry_fields[table_name] = {}
        
        for i, field in enumerate(field_names):
            row_frame = Frame(form_frame)
            row_frame.pack(fill="x", pady=2)
            
            Label(row_frame, text=field.capitalize() + ":", width=12, anchor='w').pack(side="left")
            
            if field == 'unidad':
                combo = Combobox(row_frame, values=self.valid_units, state="readonly")
                combo.pack(side="left", expand=True, fill="x")
                self.entry_fields[table_name][field] = combo
            elif field == 'tipo':
                combo = Combobox(row_frame, values=self.valid_types, state="readonly")
                combo.pack(side="left", expand=True, fill="x")
                self.entry_fields[table_name][field] = combo
            else:
                entry = Entry(row_frame, width=50)
                entry.pack(side="left", expand=True, fill="x")
                self.entry_fields[table_name][field] = entry

        # Botones de acción
        button_frame = Frame(parent_frame, padding=10)
        button_frame.pack(fill="x", pady=10)

        Button(button_frame, text="Guardar", command=lambda: self.save_item(table_name)).pack(side="left", padx=5)
        Button(button_frame, text="Actualizar", command=lambda: self.update_item(table_name)).pack(side="left", padx=5)
        Button(button_frame, text="Eliminar", command=lambda: self.delete_item(table_name)).pack(side="left", padx=5)
        Button(button_frame, text="Limpiar Campos", command=lambda: self.clear_fields(table_name)).pack(side="left", padx=5)

        # Treeview para mostrar los datos
        tree_frame = Frame(parent_frame, padding=10)
        tree_frame.pack(pady=10, expand=True, fill="both")

        self.treeviews[table_name] = Treeview(tree_frame, columns=field_names, show="headings")
        self.treeviews[table_name].pack(expand=True, fill="both")
        
        for col in field_names:
            self.treeviews[table_name].heading(col, text=col.capitalize())
            self.treeviews[table_name].column(col, width=100)
            
        self.treeviews[table_name].bind("<<TreeviewSelect>>", self.on_item_select)
        
        self.refresh_treeview(table_name)
    
    def setup_generic_ui(self, parent_frame, table_name):
        """Configuración genérica para otras tablas, solo muestra la tabla."""
        tree_frame = Frame(parent_frame, padding=10)
        tree_frame.pack(pady=10, expand=True, fill="both")
        
        self.treeviews[table_name] = Treeview(tree_frame)
        self.treeviews[table_name].pack(expand=True, fill="both")
        
        data = get_all_data(table_name)
        if data:
            columns = list(data[0].keys())
            self.treeviews[table_name]["columns"] = columns
            for col in columns:
                self.treeviews[table_name].heading(col, text=col)
                self.treeviews[table_name].column(col, width=100)
            for item in data:
                self.treeviews[table_name].insert("", END, values=list(item.values()))

    def on_item_select(self, event):
        """Carga los datos del elemento seleccionado en los campos de entrada."""
        selected_item = self.treeviews['materiales'].focus()
        if selected_item:
            values = self.treeviews['materiales'].item(selected_item, 'values')
            field_names = ['codigo', 'descripcion', 'unidad', 'precio', 'peso', 'tipo']
            for i, field in enumerate(field_names):
                # Utiliza .set() para Combobox y .delete/.insert para Entry
                if field == 'unidad' or field == 'tipo':
                    self.entry_fields['materiales'][field].set(values[i])
                else:
                    self.entry_fields['materiales'][field].delete(0, END)
                    self.entry_fields['materiales'][field].insert(0, values[i])
            self.selected_item = values[0] # Guarda el código para las operaciones de actualización y eliminación
        
    def refresh_treeview(self, table_name):
        """Refresca la Treeview con los datos más recientes."""
        for item in self.treeviews[table_name].get_children():
            self.treeviews[table_name].delete(item)
            
        data = get_all_data(table_name)
        if data:
            for item in data:
                self.treeviews[table_name].insert("", END, values=list(item.values()))

    def clear_fields(self, table_name):
        """Limpia todos los campos de entrada."""
        for field in self.entry_fields[table_name].values():
            if isinstance(field, Combobox):
                field.set('')
            else:
                field.delete(0, END)
        self.selected_item = None

    def transform_data(self, data):
        """Transforma los datos de entrada a mayúsculas y aplica formato al código."""
        # Convertir campos de texto a mayúsculas
        for field in ['codigo', 'descripcion', 'unidad', 'tipo']:
            if field in data and isinstance(data[field], str):
                data[field] = data[field].upper()
        
        # Formatear el código para incluir un guion si no existe, respetando el formato de 9 caracteres
        if 'codigo' in data:
            codigo = data['codigo'].replace('-', '') # Elimina cualquier guion existente
            if len(codigo) == 8:
                # Inserta el guion después de los primeros 4 caracteres
                data['codigo'] = f"{codigo[:4]}-{codigo[4:]}"
        
        return data

    def save_item(self, table_name):
        """Guarda un nuevo registro en la base de datos."""
        data = {field: entry.get() for field, entry in self.entry_fields[table_name].items()}
        data = self.transform_data(data) # Aplicar transformaciones antes de guardar
        if insert_data(table_name, data):
            self.refresh_treeview(table_name)
            self.clear_fields(table_name)
    
    def update_item(self, table_name):
        """Actualiza un registro existente."""
        if self.selected_item:
            data = {field: entry.get() for field, entry in self.entry_fields[table_name].items()}
            data = self.transform_data(data) # Aplicar transformaciones antes de actualizar
            where_clause = {'codigo': self.selected_item}
            if update_data(table_name, data, where_clause):
                self.refresh_treeview(table_name)
                self.clear_fields(table_name)
        else:
            messagebox.showwarning("Advertencia", "Selecciona un elemento para actualizar.")
            
    def delete_item(self, table_name):
        """Elimina un registro existente."""
        if self.selected_item:
            if messagebox.askyesno("Confirmar Eliminación", "¿Estás seguro de que quieres eliminar este registro?"):
                where_clause = {'codigo': self.selected_item}
                if delete_data(table_name, where_clause):
                    self.refresh_treeview(table_name)
                    self.clear_fields(table_name)
        else:
            messagebox.showwarning("Advertencia", "Selecciona un elemento para eliminar.")


def main():
    root = Tk()
    app = ProjectApp(root)
    root.mainloop()

if __name__ == '__main__':
    main()