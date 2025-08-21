# modelos.py

class Material:
    def __init__(self, codigo, descripcion, unidad, precio, peso):
        self.codigo = codigo
        self.descripcion = descripcion
        self.unidad = unidad
        self.precio = precio
        self.peso = peso

    def __str__(self):
        return f"{self.codigo} | {self.descripcion} | {self.unidad} | ${self.precio:,2f} | {self.peso:,2f}"


class ManoDeObra:
    def __init__(self, codigo, descripcion, unidad, valor_unitario):
        self.codigo = codigo
        self.descripcion = descripcion
        self.unidad = unidad
        self.valor_unitario = valor_unitario
    def __str__(self):
        return f"{self.codigo} | {self.descripcion} | {self.unidad} | ${self.valor_unitario:,.2f}"

class Herramienta:
    def __init__(self, codigo, descripcion, unidad, valor_unitario):
        self.codigo = codigo
        self.descripcion = descripcion
        self.unidad = unidad
        self.valor_unitario = valor_unitario

    def __str__(self):
        return f"{self.codigo} | {self.descripcion} | {self.unidad} | ${self.valor_unitario:,.2f}"


class Transporte:
    def __init__(self, codigo, descripcion, unidad, precio):
        self.codigo = codigo
        self.descripcion = descripcion
        self.unidad = unidad
        self.precio = precio

    def __str__(self):
        return f"{self.codigo} | {self.descripcion} | {self.unidad} | ${self.precio:,.2f}"