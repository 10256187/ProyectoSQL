import os
import unittest
from gestor import GestorMaterialesSQLite

class TestGestorMateriales(unittest.TestCase):

    def setUp(self):
        self.test_db = "test_materiales.db"
        # Asegúrate de que no exista antes
        if os.path.exists(self.test_db):
            os.remove(self.test_db)
        self.gestor = GestorMaterialesSQLite(nombre_db=self.test_db)

    def tearDown(self):
        del self.gestor  # Cierra cualquier conexión
        if os.path.exists(self.test_db):
            os.remove(self.test_db)

    def test_agregar_material(self):
        self.gestor.agregar_material_manual(
            codigo="TEST-0001",
            descripcion="Material de prueba",
            unidad="KG",
            precio=1234.56,
            peso= 0.25
        )

        materiales = self.gestor.ver_materiales()
        self.assertEqual(len(materiales), 1)
        self.assertEqual(materiales[0][0], "TEST-0001")

if __name__ == '__main__':
    unittest.main()