import pymysql

def get_existe_llamada(conn,codigo_cama ):
    ''' consuta para saber si una cama tiene una llamada activa'''
    try:
        cursor = conn.cursor()
        cursor.execute(
            '''
            SELECT *
            FROM llamada l
            JOIN cama c ON l.codigo_cama = c.codigo
            WHERE c.codigo = %s and l.estado = 0;
            ''',
            (codigo_cama,)
        )
        resultado = cursor.fetchone() 
        return {"exito":True, "mensaje": resultado}
    except pymysql.Error as e:
        return {"exito":False, "mensaje":e}
    finally:
        if cursor:
            cursor.close()

def get_lampara(conn,codigo_cama ):
    '''funcion que obitene los datos de la cama a partir del codigo'''
    try:
        cursor = conn.cursor()
        cursor.execute(
            '''
            SELECT lampara
            FROM cama 
            WHERE codigo = %s;
            ''',
            (codigo_cama,)
        )
        salida = cursor.fetchone()
        return salida['lampara'] # se devuelve el resultado de la consulta
    except pymysql.Error as e:
        return e
    finally:
        if cursor:
            cursor.close()

def get_id_asistente (conn, codigo_acceso):
    
    try:
        cursor = conn.cursor()
        cursor.execute(
            '''
            SELECT id
            FROM asistente
            WHERE codigo_acceso = %s;
            ''',
            (codigo_acceso,)
        )

        resultado = cursor.fetchone()
        return {"exito":True, "mensaje": resultado}
    except pymysql.Error as e:
        return {"exito":False, "mensaje":e}
    finally:
        if cursor:
            cursor.close()