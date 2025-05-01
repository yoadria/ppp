
import pymysql
import logging
import os
import time
logging.basicConfig(
    level=logging.DEBUG,  # Muestra los logs de nivel DEBUG y superior
    format='%(asctime)s - %(levelname)s - %(message)s'  # Formato para mostrar los logs
)

_logging = logging.getLogger(__name__)


# Configuración de la base de datos (ajusta con tus credenciales de Docker Compose)
DB_HOST = os.environ.get('DB_HOST', 'mariadb')
DB_USER = os.environ.get('DB_USER', 'admin')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'admin')
DB_NAME = os.environ.get('DB_NAME', 'hospital_call')


    
def get_db_connection(max_retries=10, delay=3):
    '''inicializa la conexión con reintentos'''
    retries = 0

    while retries < max_retries:
        try:
            conn = pymysql.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME,
                cursorclass=pymysql.cursors.DictCursor
            )
            _logging.info("✅ Conexión a la base de datos inicializada")
            return conn
        except pymysql.err.OperationalError as e:
            _logging.warning(f"⚠️ Intento {retries+1}: Error al conectar a la base de datos: {e}")
            retries += 1
            time.sleep(delay)

    _logging.error("❌ No se pudo conectar a la base de datos tras varios intentos")
    raise Exception("No se pudo conectar a la base de datos")


