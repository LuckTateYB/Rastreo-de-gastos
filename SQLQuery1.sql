create database rastreo_gastos;
use rastreo_gastos;

CREATE TABLE Gastos (
    Id INT IDENTITY(1,1) PRIMARY KEY,
    Descripcion NVARCHAR(255) NOT NULL,
    Monto DECIMAL(10, 2) NOT NULL,
    Categoria NVARCHAR(50) NOT NULL,
    Fecha DATE NOT NULL
);

INSERT INTO Gastos (Descripcion, Monto, Categoria, Fecha)
VALUES ('Compra de snacks', 10.50, 'Comida', '2024-12-07');

select* from Gastos;

