# -*- coding: utf-8 -*-
"""
Este módulo centraliza todas las constantes de la aplicación, como las unidades
y tipos de materiales válidos.
"""

# Constantes para las unidades y tipos de cada categoría
UNIDADES = {
    "material":    ['UN', 'ML', 'KM', 'LB', 'KG', 'TN', 'SC', 'GL', 'GB', 'PG', 'M2', 'M3', 'LT'],
    "mobra":       ['HH', 'DD', 'MS', 'JN', 'VT', 'CM'],
    "herramienta": ['HR', 'DD', 'MS', 'VJ', 'M³'],
    "transporte":  ['VJ', 'M³', 'MS', 'DD', 'HR', 'TK'],
    "unitario":  ['VJ', 'M³', 'MS', 'DD', 'HR', 'TK']
}

TIPOS_MATERIALES = ('MAR', 'HIE', 'CEM', 'CON', 'HER', 'CAB', 'ESM', 'ESC', 'ELE', 'ILU', 'CPM', 'CAP')
