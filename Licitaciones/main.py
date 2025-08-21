import typer
from rich.console import Console
from validaciones import leer_codigo, leer_descripcion, leer_unidad, leer_valor_numerico
from gestor import (
    gestor_materiales,
    gestor_mano_obra,
    gestor_herramientas,
    gestor_transporte,
    gestor_estructura
)

app = typer.Typer()
console = Console()

# ======== MATERIALES ========
@app.command()
def agregar_material():
    """Agregar un nuevo material"""
    console.print("🔹 Agregar Material 🔹", style="bold green")
    codigo = leer_codigo()
    descripcion = leer_descripcion()
    unidad = leer_unidad("material")
    precio = leer_valor_numerico()
    gestor_materiales.agregar(codigo, descripcion, unidad, precio)

@app.command()
def ver_materiales():
    """Ver todos los materiales"""
    gestor_materiales.ver()

@app.command()
def editar_material():
    """Editar un material"""
    console.print("✏️ Editar Material", style="bold yellow")
    codigo = leer_codigo()
    descripcion = leer_descripcion()
    unidad = leer_unidad("material")
    precio = leer_valor_numerico()
    gestor_materiales.editar(codigo, descripcion, unidad, precio)

# ======== MANO DE OBRA ========
@app.command()
def agregar_mano_obra():
    """Agregar mano de obra"""
    console.print("🔹 Agregar Mano de Obra 🔹", style="bold green")
    codigo = leer_codigo()
    descripcion = leer_descripcion()
    unidad = leer_unidad("mano_obra")
    precio = leer_valor_numerico()
    gestor_mano_obra.agregar(codigo, descripcion, unidad, precio)

@app.command()
def ver_mano_obra():
    """Ver mano de obra"""
    gestor_mano_obra.ver()

@app.command()
def editar_mano_obra():
    """Editar mano de obra"""
    console.print("✏️ Editar Mano de Obra", style="bold yellow")
    codigo = leer_codigo()
    descripcion = leer_descripcion()
    unidad = leer_unidad("mano_obra")
    precio = leer_valor_numerico()
    gestor_mano_obra.editar(codigo, descripcion, unidad, precio)

# ======== HERRAMIENTAS ========
@app.command()
def agregar_herramienta():
    """Agregar herramienta"""
    console.print("🔹 Agregar Herramienta 🔹", style="bold green")
    codigo = leer_codigo()
    descripcion = leer_descripcion()
    unidad = leer_unidad("herramienta")
    precio = leer_valor_numerico()
    gestor_herramientas.agregar(codigo, descripcion, unidad, precio)

@app.command()
def ver_herramientas():
    """Ver herramientas"""
    gestor_herramientas.ver()

@app.command()
def editar_herramienta():
    """Editar herramienta"""
    console.print("✏️ Editar Herramienta", style="bold yellow")
    codigo = leer_codigo()
    descripcion = leer_descripcion()
    unidad = leer_unidad("herramienta")
    precio = leer_valor_numerico()
    gestor_herramientas.editar(codigo, descripcion, unidad, precio)

# ======== TRANSPORTE ========
@app.command()
def agregar_transporte():
    """Agregar transporte"""
    console.print("🔹 Agregar Transporte 🔹", style="bold green")
    codigo = leer_codigo()
    descripcion = leer_descripcion()
    unidad = leer_unidad("transporte")
    precio = leer_valor_numerico()
    gestor_transporte.agregar(codigo, descripcion, unidad, precio)

@app.command()
def ver_transporte():
    """Ver transporte"""
    gestor_transporte.ver()

@app.command()
def editar_transporte():
    """Editar transporte"""
    console.print("✏️ Editar Transporte", style="bold yellow")
    codigo = leer_codigo()
    descripcion = leer_descripcion()
    unidad = leer_unidad("transporte")
    precio = leer_valor_numerico()
    gestor_transporte.editar(codigo, descripcion, unidad, precio)

# ======== ESTRUCTURA ========
@app.command()
def agregar_estructura():
    """Agregar estructura"""
    console.print("🔹 Agregar Estructura 🔹", style="bold green")
    codigo = leer_codigo()
    descripcion = leer_descripcion()
    unidad = leer_unidad("estructura")
    precio = leer_valor_numerico()
    gestor_estructura.agregar(codigo, descripcion, unidad, precio)

@app.command()
def ver_estructura():
    """Ver estructura"""
    gestor_estructura.ver()

@app.command()
def editar_estructura():
    """Editar estructura"""
    console.print("✏️ Editar Estructura", style="bold yellow")
    codigo = leer_codigo()
    descripcion = leer_descripcion()
    unidad = leer_unidad("estructura")
    precio = leer_valor_numerico()
    gestor_estructura.editar(codigo, descripcion, unidad, precio)


if __name__ == "__main__":
    app()
