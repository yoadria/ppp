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
    

def nueva_habitacion(conn, planta, numero):
    '''se inserta una nueva habitacion a la base de datos'''
    try:
        cursor = conn.cursor()

        cursor.execute(
            '''
            INSERT INTO habitacion (numero, planta)
            VALUES (%s,%s)
            ''',
            (numero, planta)
        )
        conn.commit()
        _logging.debug('Habitacion creada con exito')
        return True
    except pymysql.Error as e:
        _logging.debug(f'Error al crear habitacion: {e}')
        return False
    finally:
        cursor.close()


def nueva_cama(conn, codigo, id_habitacion):
    '''se inserta una nueva cama a la base de datos'''
    try:
        cursor = conn.cursor()

        cursor.execute(
        '''
        INSERT INTO cama (codigo, id_habitacion)
        VALUES (%s,%s)
        ''',
        (codigo, id_habitacion)
        )
        conn.commit()
        _logging.debug('Cama creada con exito')
        return True
    
    except pymysql.Error as e:
        _logging.debug(f'Error al crear cama: {e}')
        return False
    finally:
        cursor.close()

def crear_llamada(conn,id):
    try:
        cursor = conn.cursor()
        cursor.execute(
            '''
            INSERT INTO llamada (id_cama)
            VALUES (%s)
            ''',
            (id)
        )
        conn.commit()
        return {'exito': True, 'mensaje': 'llamada creada con exito'}
    except pymysql.Error as e:
        return {'exito': False, 'mensaje': e}
    finally:
        cursor.close()

def nueva_presencia(conn, id_llamada):
    try:
        cursor = conn.cursor()
        # Obtener el id_asistente de la llamada
        cursor.execute(
            '''
            SELECT id_asistente FROM llamada WHERE id = %s
            ''',
            (id_llamada,)
        )
        resultado = cursor.fetchone()
        if not resultado or not resultado['id_asistente']:
            return {'exito': False, 'mensaje': 'No se encontró id_asistente para esa llamada'}
        id_asistente = resultado['id_asistente']

        # Insertar en presencia
        cursor.execute(
            '''
            INSERT INTO presencia (id_llamada, id_asistente)
            VALUES (%s, %s)
            ''',
            (id_llamada, id_asistente)
        )
        conn.commit()
        _logging.debug('Presencia creada con exito')
        return {'exito': True, 'mensaje': 'Presencia creada con exito'}
    except pymysql.Error as e:
        _logging.debug('Error al crear presencia: %s', e)
        return {'exito': False, 'mensaje': e}
    finally:
        cursor.close()