import pymysql
import logging

logging.basicConfig(
    level=logging.DEBUG,  # Muestra los logs de nivel DEBUG y superior
    format='%(asctime)s - %(levelname)s - %(message)s'  # Formato para mostrar los logs
)
_logging = logging.getLogger(__name__)

def actualizar_receip_llamada(conn, codigo_cama, receip_id):
    try:
        cursor = conn.cursor()
        cursor.execute(
            '''
            UPDATE llamada
            SET receipt_id = %s
            WHERE codigo_cama = %s and esatdo =0;
            '''
            (receip_id, codigo_cama)
        )
        conn.commit()
        _logging.debug('receipt id actualizaco')
        return {'exito': True, 'mensaje': 'receipt id actualizado'}
    except pymysql.Error as e:
        _logging.debug(f'Error al actualizar receipt id: {e}')
        return {'exito': False, 'mensaje': e}
    finally:
        cursor.close()