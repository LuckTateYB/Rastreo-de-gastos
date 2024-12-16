**RASTREO DE GASTOS(TRACKPAYS)**

*Descripción:*

El proyecto se basa en la recolección de información de gastos del usuario permitiendole saber el total gastado.

*Requisitos:*

 * Python: Versión 3.12.5 o superior
 * Flask: Última versión
 * SQLAlchemy: Para la interacción con la base de datos
 * Werkzeug: Para el manejo y seguridad de contraseñas
   
*Instalación:*

 * Clonar el repositorio:
   
   git clone https://github.com/LuckTateYB/Rastreo-de-gastos.git

 * Crear un entorno virtual (recomendado):
   
   python -m venv venv
   
source venv/bin/activate  # En Linux/macOS

venv\Scripts\activate  # En Windows

 * Instalar las dependencias:
   
   pip install -r requirements.txt

*Estructura del proyecto:*

 * app.py: Archivo principal de la aplicación Flask.
 * templates: Contiene las plantillas HTML.
 * static: Contiene archivos estáticos como CSS y JavaScript.

Contribuciones:
Este proyecto quiero hacerlo escalable y que su funcionalidad pase de ser manual a automatica con API's.
Al ser entidades bancarias no es fácil utilizarlas, pero sería interesante crear una propia para testear su funcionamiento.

Requirements:

- Flask
- SQLAlchemy
- Werkzeug

*Aspectos adicionales a considerar:*

 * Base de datos: El driver es para SQLServer
 * Configuración:
   create database (nombre_de_preferencia)
   use (database) 
   CREATE TABLE Usuarios (
      id INT PRIMARY KEY IDENTITY(1,1),
      username NVARCHAR(50) UNIQUE NOT NULL,
      password NVARCHAR(255) NOT NULL
    );

    CREATE TABLE Gastos (
      id INT PRIMARY KEY IDENTITY(1,1),
      descripcion NVARCHAR(100) NOT NULL,
      monto FLOAT NOT NULL,
      categoria NVARCHAR(50) NOT NULL,
      fecha DATE NOT NULL,
      user_id INT NOT NULL,
      FOREIGN KEY (user_id) REFERENCES Usuarios(id)
    );

 
![image](https://github.com/user-attachments/assets/ca18d2de-cec6-4b4d-973a-448eb57ef8d6)


![image](https://github.com/user-attachments/assets/0968d449-1c3c-470a-a7ca-5b7f95d341b9)


![image](https://github.com/user-attachments/assets/e198c519-7bc7-4721-a489-196c70cabd6d)
