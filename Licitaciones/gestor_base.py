# gestor_base.py
import sqlite3
import csv
from rich.console import Console
from rich.table import Table

class GestorBaseSQLite:
    def __init__(self, nombre_db, nombre_tabla, campos):
        self.nombre_db = nombre_db
        self.nombre_tabla = nombre_tabla
        self.campos = campos  
        
    def crear_tabla(self):
        raise NotImplementedError("Este método debe ser implementado en la subclase.")

    def agregar(self, **datos):
        conexion = sqlite3.connect(self.nombre_db)
        cursor = conexion.cursor()
        columnas = ", ".join(self.campos)
        valores = ", ".join(["?"] * len(self.campos))
        datos_ordenados = [datos[campo] for campo in self.campos]
        cursor.execute(
            f"INSERT INTO {self.nombre_tabla} ({columnas}) VALUES ({valores})",
            datos_ordenados
        )
        conexion.commit()
        conexion.close()

    def ver(self):
        conexion = sqlite3.connect(self.nombre_db)
        cursor = conexion.cursor()
        cursor.execute(f"SELECT * FROM {self.nombre_tabla}")
        resultados = cursor.fetchall()
        conexion.close()
        return resultados

    def editar(self, codigo, **nuevos_datos):
        conexion = sqlite3.connect(self.nombre_db)
        cursor = conexion.cursor()
        campos_a_actualizar = [campo for campo in self.campos if campo != "codigo"]
        actualizaciones = ", ".join([f"{campo} = ?" for campo in campos_a_actualizar])
        valores = [nuevos_datos[campo] for campo in campos_a_actualizar]
        valores.append(codigo)
        cursor.execute(
            f"UPDATE {self.nombre_tabla} SET {actualizaciones} WHERE codigo = ?",
            valores
        )
        conexion.commit()
        conexion.close()
        
    def eliminar(self, codigo):
        conexion = sqlite3.connect(self.nombre_db)
        cursor = conexion.cursor()
        cursor.execute(f"DELETE FROM {self.nombre_tabla} WHERE codigo = ?", (codigo,))
        conexion.commit()
        conexion.close()

    def exportar_csv(self, nombre_archivo):
        conexion = sqlite3.connect(self.nombre_db)
        cursor = conexion.cursor()
        cursor.execute(f"SELECT * FROM {self.nombre_tabla}")
        filas = cursor.fetchall()
        conexion.close()

        with open(nombre_archivo, mode="w", newline="", encoding="utf-8") as archivo:
            escritor = csv.writer(archivo)
            escritor.writerow(self.campos)
            escritor.writerows(filas)
