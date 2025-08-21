import re

class Recurso:
    def __init__(self, codigo, descripcion, unidad, valor):
        self.codigo = self.validar_codigo(codigo)
        self.descripcion = descripcion
        self.unidad = self.validar_unidad(unidad)
        self.valor = valor

    def validar_codigo(self, codigo):
        codigo = codigo.strip().upper()
        if re.match(r"^[A-Z]{4}\d{4}$", codigo):
            codigo = codigo[:4] + "-" + codigo[4:]
        if not re.match(r"^[A-Z]{4}-\d{4}$", codigo):
            raise ValueError("❌ Código inválido. Debe ser AAAA-NNNN.")
        return codigo

    def validar_unidad(self, unidad):
        if not re.match(r"^[A-Za-z][A-Za-z0-9]$", unidad):
            raise ValueError("❌ Unidad inválida. Debe tener 2 caracteres.")
        return unidad

    def mostrar_info(self):
        print(f"{self.codigo} | {self.descripcion} | {self.unidad} | ${self.valor}")

#Clases hijas

class Material(Recurso):
    def __init__(self, codigo, descripcion, unidad, valor, peso):
        super().__init__(codigo, descripcion, unidad, valor)
        self.peso = peso

    def mostrar_info(self):
        print(f"{self.codigo} | {self.descripcion} | {self.unidad} | ${self.valor} | {self.peso}kg")


class ManoDeObra(Recurso):
    def __init__(self, codigo, descripcion, unidad, valor, horas=0):
        super().__init__(codigo, descripcion, unidad, valor)
        self.horas = horas

    def mostrar_info(self):
        print(f"{self.codigo} | {self.descripcion} | {self.unidad} | ${self.valor} | {self.horas} horas")


class Herramienta(Recurso):
    def __init__(self, codigo, descripcion, unidad, valor):
        super().__init__(codigo, descripcion, unidad, valor)


class Transporte(Recurso):
    def __init__(self, codigo, descripcion, unidad, valor):
        super().__init__(codigo, descripcion, unidad, valor)


if __name__ == "__main__":
    m1 = Material("abcd1234", "Cemento Gris", "Kg", 1800, 50)
    m2 = ManoDeObra("pers0001", "Oficial de obra", "Hr", 25000, 8)
    m3 = Herramienta("hrrt0001", "Taladro", "Un", 90000)
    m4 = Transporte("tran0001", "Camión de Volteo", "Vj", 120000)

    recursos = [m1, m2, m3, m4]

    for r in recursos:
        r.mostrar_info()
