from flask import Flask
import pymysql
import logging

_logging = logging.getLogger(__name__)

app = Flask(__name__)

# Configuración de la base de datos (ajusta con tus credenciales de Docker Compose)
#DB_HOST = 'mariadb'  # El nombre del servicio de MariaDB en Docker
DB_HOST = '127.0.0.1'
DB_USER = 'myuser'
DB_PASSWORD = 'mypass'
DB_NAME = 'pruebadb'

def crear_tabla_llamadas():
    conn = None  # Inicializa la conexión a None para manejar el bloque finally
    try:
        # Conectar a la base de datos
        conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
        cursor = conn.cursor()

        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS prueba1 (
                id INT AUTO_INCREMENT PRIMARY KEY,
                campo_1 VARCHAR(10) NOT NULL,
                campo_2 CHAR(1) NOT NULL,
                campo_3 VARCHAR(10),
                campo_4 VARCHAR(10),
                campo_5 VARCHAR(10)
            )
        """)

        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS prueba2 (
                id INT AUTO_INCREMENT PRIMARY KEY,
                campo_1 VARCHAR(10) NOT NULL,
                campo_2 CHAR(1) NOT NULL,
                campo_3 VARCHAR(10),
                campo_4 VARCHAR(10),
                campo_5 VARCHAR(10),
                id_prueba1 INT NOT NULL,
                FOREIGN KEY (id_prueba1) REFERENCES prueba1(id) ON DELETE CASCADE 
            )
        """)

        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS prueba3 (
                id INT AUTO_INCREMENT PRIMARY KEY,
                campo_1 VARCHAR(10) NOT NULL,
                campo_2 CHAR(1) NOT NULL,
                campo_3 VARCHAR(10),
                campo_4 VARCHAR(10),
                campo_5 VARCHAR(10)
            )
        """)

        conn.commit()
        _logging.info("Tablas creadas")
        print("ok")

    except pymysql.Error as e:
        _logging.info(f"Error al crear las tablas con PyMySQL: {e}")
        print(f"Error: {e}")

    finally:
        if conn:
            cursor.close()
            conn.close()

if __name__ == '__main__':
    with app.app_context():
        crear_tabla_llamadas()