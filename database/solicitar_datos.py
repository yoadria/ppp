import pymysql

def get_existe_llamada(conn,habitacion, cama ):
    ''' consuta para saber si una cama tiene una llamada activa'''
    try:
        cursor = conn.cursor()
        cursor.execute(
            '''
            SELECT l.*
            FROM llamada l
            JOIN cama c ON l.id_cama = c.id
            JOIN habitacion h ON c.id_habitacion = h.id
            WHERE h.numero = %s
              AND c.codigo = %s
              AND l.estado != 'finalizada';
            ''',
            (habitacion, cama)
        )
        resultado = cursor.fetchall()
        return {"exito": True, "mensaje": resultado}
    except pymysql.Error as e:
        return {"exito": False, "mensaje": e}
    finally:
        if cursor:
            cursor.close()


def get_asistente (conn, nombre, codigo):   
    try:
        cursor = conn.cursor()
        cursor.execute(
            '''
            SELECT id
            FROM asistente
            WHERE codigo_acceso = %s AND nombre = %s;
            ''',
            (codigo,nombre)
        )

        resultado = cursor.fetchone()
        return {"exito":True, "mensaje": resultado}
    except pymysql.Error as e:
        return {"exito":False, "mensaje":e}
    finally:
        if cursor:
            cursor.close()

def get_id_cama(conn,habitacion,cama):

    try:
        cursor = conn.cursor()
        cursor.execute(
            '''
            SELECT c.id
            FROM cama c
            JOIN habitacion h ON c.id_habitacion = h.id
            WHERE h.numero = %s AND c.codigo = %s
            ''',
            (habitacion, cama)
        )
        resultado = cursor.fetchone()
        if resultado:
            return resultado['id']
        else:
            return None
    except pymysql.Error as e:
        return None
    finally:
        if cursor:
            cursor.close()

def get_id_llamada(conn, habitacion, cama):
    try:
        cursor = conn.cursor()
        cursor.execute(
            '''
            SELECT l.id
            FROM llamada l
            JOIN cama c ON l.id_cama = c.id
            JOIN habitacion h ON c.id_habitacion = h.id
            WHERE h.numero = %s
              AND c.codigo = %s
              AND l.estado = 'solicitar';
            ''',
            (habitacion, cama)
        )
        resultado = cursor.fetchone()
        if resultado and 'id' in resultado:
            return resultado['id']
        else:
            return False
    except pymysql.Error as e:
        return False
    finally:
        if cursor:
            cursor.close()

def get_id_llamada_aceptada(conn, habitacion, cama):
    try:
        cursor = conn.cursor()
        cursor.execute(
            '''
            SELECT l.id
            FROM llamada l
            JOIN cama c ON l.id_cama = c.id
            JOIN habitacion h ON c.id_habitacion = h.id
            WHERE h.numero = %s
              AND c.codigo = %s
              AND l.estado = 'aceptada';
            ''',
            (habitacion, cama)
        )
        resultado = cursor.fetchone()
        return resultado['id']
    except pymysql.Error as e:
        return False
    finally:
        if cursor:
            cursor.close()

def get_lampara(conn, id):
    try:
        cursor = conn.cursor()
        cursor.execute(
            '''
            SELECT lampara
            FROM cama 
            WHERE id = %s
            ''',
            (id,)
        )
        resultado = cursor.fetchone()
        if resultado and 'lampara' in resultado:
            return  resultado['lampara']
        else:
            return None
    except pymysql.Error as e:
        return None
    finally:
        if cursor:
            cursor.close()

def get_historico_completo(conn, asistente=None, rango_fecha=None, estado=None):
    """
    Devuelve el histórico completo de llamadas con filtros opcionales.
    """
    try:
        cursor = conn.cursor()
        query = '''
            SELECT 
                l.id AS id_llamada,
                l.hora_llamada,
                l.hora_atendida,
                l.estado,
                a.nombre AS nombre_asistente,
                p.hora_llegada AS hora_presencia
            FROM llamada l
            LEFT JOIN asistente a ON l.id_asistente = a.id
            LEFT JOIN presencia p ON l.id = p.id_llamada
            WHERE 1=1
        '''
        params = []

        if asistente:
            query += " AND a.nombre LIKE %s"
            params.append(f"%{asistente}%")
        if estado:
            query += " AND l.estado = %s"
            params.append(estado)
        if rango_fecha and rango_fecha != "all":
            if rango_fecha == "24h":
                query += " AND l.hora_llamada >= NOW() - INTERVAL 1 DAY"
            elif rango_fecha == "7d":
                query += " AND l.hora_llamada >= NOW() - INTERVAL 7 DAY"
            elif rango_fecha == "1m":
                query += " AND l.hora_llamada >= NOW() - INTERVAL 1 MONTH"
            elif rango_fecha == "3m":
                query += " AND l.hora_llamada >= NOW() - INTERVAL 3 MONTH"

        query += " ORDER BY l.id DESC"

        cursor.execute(query, params)
        resultado = cursor.fetchall()
        return {"exito": True, "mensaje": resultado}
    except pymysql.Error as e:
        return {"exito": False, "mensaje": e}
    finally:
        if cursor:
            cursor.close()


def get_id_habitacion(conn, planta, numero):
    try:

        cursor = conn.cursor()
        cursor.execute(
            '''
                SELECT id
                FROM habitacion
                WHERE numero = %s AND planta = %s;
            ''',
            (numero,planta)
        )

        id = cursor.fetchone()
        if id:
            return id['id']
        else:
            return False
    except pymysql.Error as e:
        return False
    finally:
        cursor.close