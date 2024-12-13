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

CREATE TABLE Usuarios (
    Id INT IDENTITY(1,1) PRIMARY KEY,
    Username NVARCHAR(50) NOT NULL UNIQUE,
    Password NVARCHAR(255) NOT NULL
);

ALTER TABLE Gastos
ADD UserId INT;

ALTER TABLE Gastos
ADD CONSTRAINT FK_Gastos_Usuarios FOREIGN KEY (UserId) REFERENCES Usuarios(Id) ON DELETE CASCADE;

-- Insertar datos de ejemplo para Usuarios
INSERT INTO Usuarios (Username, Password)
VALUES ('usuario1', 'password1'), ('usuario2', 'password2');

-- Insertar datos de ejemplo para Gastos relacionados con Usuarios
INSERT INTO Gastos (Descripcion, Monto, Categoria, Fecha, UserId)
VALUES 
('Compra de snacks', 10.50, 'Comida', '2024-12-07', 1),
('Compra de ropa', 150.00, 'Vestimenta', '2024-12-09', 2);
