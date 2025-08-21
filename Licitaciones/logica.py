from validaciones import leer_codigo, leer_descripcion, leer_unidad, leer_valor_unitario
from gestor import GestorMaterialesSQLite

gestor_materiales = GestorMaterialesSQLite("datos.db")

def agregar_material(data):
    # Validaciones
    codigo = leer_codigo(data["codigo"])
    descripcion = leer_descripcion(data["descripcion"])
    unidad = leer_unidad("material", data["unidad"])
    precio = leer_valor_unitario(data["precio"])

    # Guardar
    gestor_materiales.agregar(codigo, descripcion, unidad, precio)
    return True