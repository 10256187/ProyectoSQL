import typer

from gestores import (
    GestorMaterialesSQLite,
    GestorManoObraSQLite,
    GestorHerramientasSQLite,
    GestorTransporteSQLite,
)

app = typer.Typer(help="📦 Sistema de gestión de insumos para licitaciones.")

material_app = typer.Typer()
mano_obra_app = typer.Typer()
herramienta_app = typer.Typer()
transporte_app = typer.Typer()

materiales = GestorMaterialesSQLite()
mano_obra = GestorManoObraSQLite()
herramientas = GestorHerramientasSQLite()
transporte = GestorTransporteSQLite()

# Comandos para Materiales
@material_app.command("agregar")
def agregar_material():
    materiales.agregar_material()

@material_app.command("ver")
def ver_materiales():
    materiales.ver_materiales()

@material_app.command("editar")
def editar_material():
    materiales.editar_material()

# Comandos para Mano de Obra
@mano_obra_app.command("agregar")
def agregar_mano_obra():
    mano_obra.agregar_mano_obra()

@mano_obra_app.command("ver")
def ver_mano_obra():
    mano_obra.ver_mano_obra()

@mano_obra_app.command("editar")
def editar_mano_obra():
    mano_obra.editar_mano_obra()

# Comandos para Herramientas
@herramienta_app.command("agregar")
def agregar_herramienta():
    herramientas.agregar_herramienta()

@herramienta_app.command("ver")
def ver_herramientas():
    herramientas.ver_herramientas()

@herramienta_app.command("editar")
def editar_herramienta():
    herramientas.editar_herramienta()

# Comandos para Transporte
@transporte_app.command("agregar")
def agregar_transporte():
    transporte.agregar_transporte()

@transporte_app.command("ver")
def ver_transporte():
    transporte.ver_transporte()

@transporte_app.command("editar")
def editar_transporte():
    transporte.editar_transporte()

# Agregar subaplicaciones a la aplicación principal
app.add_typer(material_app, name="material", help="📄 Gestión de materiales")
app.add_typer(mano_obra_app, name="mano-obra", help="🧑‍🔧 Gestión de mano de obra")
app.add_typer(herramienta_app, name="herramienta", help="🛠️ Gestión de herramientas")
app.add_typer(transporte_app, name="transporte", help="🚚 Gestión de transporte")

if __name__ == "__main__":
    app()