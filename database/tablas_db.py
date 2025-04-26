from flask import Flask
import pymysql
import logging

_logging = logging.getLogger(__name__)

app = Flask(__name__)


def crear_tabla_llamadas(conn):
    try:
        # Conectar a la base de datos
        cursor = conn.cursor()

        # Sentencias SQL para crear las tablas (DDL)
        cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS habitacion (
            id INT AUTO_INCREMENT PRIMARY KEY,
            numero INT NOT NULL,
            planta INT NOT NULL
        );
        '''
        )
        

        cursor.execute(
        '''
            CREATE TABLE IF NOT EXISTS cama (
                id INT AUTO_INCREMENT PRIMARY KEY,
                codigo VARCHAR(10) UNIQUE NOT NULL, -- Ejemplo: '104B', '205A'
                id_habitacion INT NOT NULL,
                FOREIGN KEY (id_habitacion) REFERENCES habitacion(id) ON DELETE CASCADE
            );
        '''
        ) 

        cursor.execute(
        '''
            CREATE TABLE IF NOT EXISTS asistente (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL,
                codigo_acceso VARCHAR(10) UNIQUE NOT NULL
                -- NOTA: En un sistema real, almacenar la clave HASHED, no en texto plano.
            );
        '''
        )

        cursor.execute(
        '''
            CREATE TABLE IF NOT EXISTS llamada (
                id INT AUTO_INCREMENT PRIMARY KEY,
                hora_llamada TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                hora_asignacion TIMESTAMP NULL,
                id_cama INT NOT NULL,
                id_asistente INT NULL,
                estado ENUM('espera', 'asignada', 'atendida') DEFAULT 'espera' NOT NULL,
                FOREIGN KEY (id_cama) REFERENCES cama(id) ON DELETE CASCADE,
                FOREIGN KEY (id_asistente) REFERENCES asistente(id) ON DELETE SET NULL
            );
        '''
        )

        cursor.execute(
        '''
            CREATE TABLE IF NOT EXISTS presencia (
                id INT AUTO_INCREMENT PRIMARY KEY,
                hora_llegada TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                id_llamada INT UNIQUE NOT NULL,
                id_asistente INT NOT NULL,
                FOREIGN KEY (id_llamada) REFERENCES llamada(id) ON DELETE CASCADE,
                FOREIGN KEY (id_asistente) REFERENCES asistente(id) ON DELETE CASCADE
            );
        '''
        )

        # Commit los cambios
        conn.commit()

        _logging.info("Tablas creadas exitosamente")
        print("Tablas creadas exitosamente")     

    except pymysql.Error as e:
        _logging.info(f"Error al crear las tablas con PyMySQL: {e}")
        print(f"Error: {e}")


    finally:
        if conn:
            if hasattr(locals(), 'cursor') and cursor: #Verifica si existe el objeto cursor
                cursor.close() #Moverlo a la sentencia finally
            conn.close() #Moverlo a la sentencia finally

