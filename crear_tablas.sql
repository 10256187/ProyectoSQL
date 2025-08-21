- Creamos la base de datos si no existe
CREATE DATABASE IF NOT EXISTS ProyectoSQL;

-- Seleccionamos la base de datos para usarla
USE ProyectoSQL;

-- Eliminamos las tablas si existen para empezar de cero
DROP TABLE IF EXISTS materiales;
DROP TABLE IF EXISTS mobra;
DROP TABLE IF EXISTS herramienta;
DROP TABLE IF EXISTS transporte;

-- Tabla de materiales
CREATE TABLE IF NOT EXISTS materiales (
    codigo VARCHAR(9) PRIMARY KEY,
    descripcion VARCHAR(255) NOT NULL,
    unidad VARCHAR(3) NOT NULL,
    precio DECIMAL(10, 2) NOT NULL,
    peso DECIMAL(10, 2),
    tipo VARCHAR(3) NOT NULL,
    -- Restricciones de validación
    CONSTRAINT chk_materiales_unidad_valida CHECK (unidad IN ('Un', 'Ml', 'kM', 'Lb', 'kG', 'Tn', 'Sc', 'Gl', 'GB', 'pg', 'M²', 'M³', 'Lt')),
    CONSTRAINT chk_materiales_precio_positivo CHECK (precio >= 0),
    CONSTRAINT chk_materiales_peso_positivo CHECK (peso >= 0),
    CONSTRAINT chk_materiales_tipo_valido CHECK (tipo IN ('MAR', 'HIE', 'CEM', 'CON', 'HER', 'CAB', 'ESM', 'ESC', 'ELE', 'ILU', 'CPM', 'CAP')),
    CONSTRAINT chk_materiales_codigo_formato CHECK (codigo REGEXP '^[A-Z]{4}-[0-9]{4}$')
);

-- Tabla de mano de obra
CREATE TABLE IF NOT EXISTS mobra (
    codigo VARCHAR(9) PRIMARY KEY,
    descripcion VARCHAR(255) NOT NULL,
    unidad VARCHAR(2) NOT NULL,
    precio DECIMAL(10, 2) NOT NULL,
    -- Restricciones de validación
    CONSTRAINT chk_mobra_unidad_valida CHECK (unidad IN ('HH', 'DD', 'MS', 'JN', 'VT', 'CM')),
    CONSTRAINT chk_mobra_precio_positivo CHECK (precio >= 0),
    CONSTRAINT chk_mobra_codigo_formato CHECK (codigo REGEXP '^[A-Z]{4}-[0-9]{4}$')
);

-- Tabla de herramientas
CREATE TABLE IF NOT EXISTS herramienta (
    codigo VARCHAR(9) PRIMARY KEY,
    descripcion VARCHAR(255) NOT NULL,
    unidad VARCHAR(3) NOT NULL,
    precio DECIMAL(10, 2) NOT NULL,
    -- Restricciones de validación
    CONSTRAINT chk_herramienta_unidad_valida CHECK (unidad IN ('HR', 'DD', 'MS', 'VJ', 'M³')),
    CONSTRAINT chk_herramienta_precio_positivo CHECK (precio >= 0),
    CONSTRAINT chk_herramienta_codigo_formato CHECK (codigo REGEXP '^[A-Z]{4}-[0-9]{4}$')
);

-- Tabla de transporte
CREATE TABLE IF NOT EXISTS transporte (
    codigo VARCHAR(9) PRIMARY KEY,
    descripcion VARCHAR(255) NOT NULL,
    unidad VARCHAR(3) NOT NULL,
    precio DECIMAL(10, 2) NOT NULL,
    -- Restricciones de validación
    CONSTRAINT chk_transporte_unidad_valida CHECK (unidad IN ('VJ', 'M³', 'MS', 'DD', 'HR', 'TKM')),
    CONSTRAINT chk_transporte_precio_positivo CHECK (precio >= 0),
    CONSTRAINT chk_transporte_codigo_formato CHECK (codigo REGEXP '^[A-Z]{4}-[0-9]{4}$')
);
-- Tabla de unitarios

