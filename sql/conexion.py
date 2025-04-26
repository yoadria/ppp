from flask import Flask
import pymysql
import logging

_logging = logging.getLogger(__name__)

app = Flask(__name__)

# Configuración de la base de datos (ajusta con tus credenciales de Docker Compose)
#DB_HOST = 'mariadb'  # El nombre del servicio de MariaDB en Docker
DB_HOST = '127.0.0.1'
DB_USER = 'admin'
DB_PASSWORD = 'admin'
DB_NAME = 'hospital_call'

def get_db_connection(app: Flask):
    try:
        conn = pymysql.connect(
            host=app.config['DB_HOST'],
            user=app.config['DB_USER'],
            password=app.config['DB_PASSWORD'],
            database=app.config['DB_NAME'],
            cursorclass=pymysql.cursors.DictCursor # Devuelve los resultados como diccionarios
        )
        return conn
    except pymysql.Error as e:
        _logging.error(f"Error al conectar a la base de datos: {e}")
        return None