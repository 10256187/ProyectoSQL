from gestor import GestorMaterialesSQLite

gestor = GestorMaterialesSQLite("materiales.db")
gestor.exportar_materiales_csv("materiales_exportados.csv")