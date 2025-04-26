
import pymysql
import logging
import os

_logging = logging.getLogger(__name__)



# Configuración de la base de datos (ajusta con tus credenciales de Docker Compose)

DB_HOST = os.environ.get('DB_HOST', '127.0.0.1')
DB_USER = os.environ.get('DB_USER', 'admin')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'admin')
DB_NAME = os.environ.get('DB_NAME', 'hospital_call')

def get_db_connection():
    try:
        conn = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            cursorclass=pymysql.cursors.DictCursor  # Devuelve los resultados como diccionarios
        )
        return conn
    except pymysql.Error as e:
        _logging.error(f"Error al conectar a la base de datos: {e}")
        return None