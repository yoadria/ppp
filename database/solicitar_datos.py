import pymysql

def get_llamada(conn,codigo_cama ):
    try:
        cursor = conn.cursor()
        cursor.execute(
            '''
            SELECT l.estado
            FROM llamada l
            JOIN cama c ON l.id_cama = c.id
            WHERE c.codigo = %s
            ORDER BY l.hora_llamada DESC
            LIMIT 1;
            ''',
            (codigo_cama,)
        )
        resultado = cursor.fetchone()
        if resultado:
            return resultado[0]
        else:
            return "No hay llamadas para esa cama"
    except pymysql.Error as e:
        return f"Error al obtener estado de llamada: {e}"
    finally:
        if cursor:
            cursor.close()