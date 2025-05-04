import pymysql
import logging

logging.basicConfig(
    level=logging.DEBUG,  # Muestra los logs de nivel DEBUG y superior
    format='%(asctime)s - %(levelname)s - %(message)s'  # Formato para mostrar los logs
)
_logging = logging.getLogger(__name__)

def nuevo_asistente(conn, datos):
    '''se inserta un nuevo asistente a la base de datos'''
    try:
        cursor = conn.cursor()
        cursor.execute(
            '''
            INSERT INTO asistente (nombre, codigo_acceso)
            VALUES (%s, %s)
            ''',
            (datos["nombre"], datos["codigo"])
        )
        conn.commit()
        _logging.debug('Asistente creado con exito')
        return {'exito': True, 'mensaje':'Asistente creada con exito'}

    except pymysql.Error as e :
        _logging.debug(f'Error al crear asistente: {e}')
        return {'exito': False, 'mensaje':e}
    finally:
        cursor.close()
    

def nueva_habitacion(conn, datos):
    '''se inserta una nueva habitacion a la base de datos'''
    try:
        cursor = conn.cursor()

        cursor.execute(
            '''
            INSERT INTO habitacion (numero, planta)
            VALUES (%s,%s)
            ''',
            (datos["numero"], datos["planta"])
        )
        conn.commit()
        _logging.debug('Habitacion creada con exito')
        return {'exito': True, 'mensaje':'Habitacion creada con exito'}
    except pymysql.Error as e:
        _logging.debug(f'Error al crear habitacion: {e}')
        return {'exito': False, 'mensaje':e}
    finally:
        cursor.close()


def nueva_cama(conn, datos):
    '''se inserta una nueva cama a la base de datos'''
    try:
        cursor = conn.cursor()

        cursor.execute(
        '''
        INSERT INTO cama (codigo, id_habitacion)
        VALUES (%s,%s)
        ''',
        (datos["codigo"], datos["id_habitacion"])
        )
        conn.commit()
        _logging.debug('Cama creada con exito')
        return {'exito': True,'mensaje':'Cama creada con exito'}
    
    except pymysql.Error as e:
        _logging.debug(f'Error al crear cama: {e}')
        return {'exito': False, 'mensaje':e}
    finally:
        cursor.close()

def crear_llamada(conn, codigo_cama):
    try:
        cursor = conn.cursor()
        cursor.execute(
            '''
            INSERT INTO llamada (codigo_cama)
            VALUES (%s)
            ''',
            (codigo_cama)
        )
        conn.commit()
        _logging.debug('llamada creada con exito')
        return {'exito': True, 'mensaje': 'llamada creada con exito'}
    except pymysql.Error as e:
        _logging.debug('Error al crear llamada: %s', e)
        return {'exito': False, 'mensaje': e}
    finally:
        cursor.close()