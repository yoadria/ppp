import pymysql
import logging

logging.basicConfig(
    level=logging.DEBUG,  # Muestra los logs de nivel DEBUG y superior
    format='%(asctime)s - %(levelname)s - %(message)s'  # Formato para mostrar los logs
)
_logging = logging.getLogger(__name__)

def llamada_atendida(conn, id_asistente, id_llamda ):
    try:
        with conn.cursor() as cursor:
            sql = """
                UPDATE llamada
                SET estado = 'aceptada',
                    id_asistente = %s,
                    hora_atendida = NOW()
                WHERE id = %s
            """
            cursor.execute(sql, (id_asistente, id_llamda))
        conn.commit()
        _logging.info(f"Llamada {id_llamda} actualizada como atendida por asistente {id_asistente}")
        return True
    except Exception as e:
        _logging.error(f"Error al actualizar la llamada: {e}")
        conn.rollback()
        return False
