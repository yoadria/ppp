from flask import Blueprint, render_template, jsonify, request, flash, redirect, url_for
from database.conexion import get_db_connection
from database.insertar_datos import *
from database.solicitar_datos import *
from .pushover_app import *
from database.actualizar_datos import *
import requests
import logging


logging.basicConfig(
    level=logging.DEBUG, 
    format='%(asctime)s - %(levelname)s - %(message)s' 
)

_logging = logging.getLogger(__name__)
main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')

@main.route('/panel_habitacion')
def panel_habitacion():
    conn = get_db_connection()
    try:
        id_cama = get_id_cama(conn, 100, 'A')
        lampara = get_lampara(conn, id_cama)
        # Si lampara es None, muestra estado desconocido
        return render_template('panelhab.html', lampara=lampara if lampara in [0, 1] else None)
    except Exception as e:
        _logging.error(f"Error en panel_habitacion: {e}")
        return render_template('panelhab.html', lampara=None)
    finally:
        conn.close()

            
@main.route('/enrolar', methods=['GET', 'POST'])
def enrolar():
    if request.method == 'POST':
        nombre = request.form['nombre_asistente']
        codigo = request.form['codigo_acceso_asistente']
        if not nombre or not codigo:
            flash('Debe ingresar un nombre y codigo', 'warning')
            return redirect(url_for('main.enrolar'))

        conn = get_db_connection()
        try:
            salida = get_asistente(conn, nombre.upper(), codigo)
            if salida['mensaje'] is None:
                flash('La clave o el nombre no son correctos', 'error')
                return redirect(url_for('main.enrolar'))

            if not salida['exito']:
                flash(f'Problemas para poder ingresar: {salida["mensaje"]}', 'error')
                return redirect(url_for('main.enrolar'))

            flash('Ha ingresado correctamente', 'success')
            return redirect(url_for('main.enrolar'))
        finally:
            conn.close()

    return render_template('enrolar.html')
   
@main.route('/formulario/asistente', methods=['GET','POST'])
def formulario_asistente():
    if request.method == 'POST':
        nombre = request.form['nombre_asistente']
        codigo = request.form['codigo_acceso_asistente']
        if not nombre or not codigo:
            flash('Uno de los campos esta vacio', 'warning')
            return redirect(url_for('main.formulario_asistente'))
        if len(codigo.replace(" ", "")) != 6:
            flash('El codigo deve tener 6 caracteres', 'warning')
            return redirect(url_for('main.formulario_asistente'))           
        
        datos = {'nombre': nombre.upper(), 'codigo': codigo}
        conn = get_db_connection()
        try:
            salida = nuevo_asistente(conn, datos)
            if salida['exito']:    
                flash(salida['mensaje'], 'success')
                return redirect(url_for('main.index'))
            else:
                flash(salida['mensaje'], 'error')
                return redirect(url_for('main.formulario_asistente'))
        finally:
            conn.close()
    return render_template('form_asistente.html')

@main.route('/formulario/habitacion', methods=['GET','POST'])
def formulario_habitacion():
    if request.method == 'POST':
        num_habitacion = request.form['numero_habitacion']
        planta = request.form['planta_habitacion']
        if not planta or not num_habitacion:
            flash('Se debe marcar una planta y un numero de habitacion', 'warning')
            return redirect(url_for('main.formulario_habitacion'))
        camas = []
        for key in request.form:
            if key.startswith('camas') and key.endswith('[identificador]'):
                camas.append(request.form[key])
        conn = get_db_connection()
        try:
            existe_habitacion = get_id_habitacion(conn, planta, num_habitacion)
            if existe_habitacion:
                flash('Ya existe la habitacion', 'warning')
                return redirect(url_for('main.formulario_habitacion'))
            salida = nueva_habitacion(conn, planta, num_habitacion)
            if salida:
                id_habitacion = get_id_habitacion(conn, planta, num_habitacion)
                for cama in camas:
                    new_cama = nueva_cama(conn,cama, id_habitacion)
                flash('Habitacion y camas creadas con exito', 'success')
                return redirect(url_for('main.index'))
            flash('Problemas al crear la habitacion o la cama', 'error')
            return redirect(url_for('main.formulario_habitacion'))
        except Exception as e:
            flash(f'Problemas con la base de datos. {e}', 'error')
            _logging.info(f'Error... {e}')
            return redirect(url_for('main.formulario_habitacion')) 
        finally:
            conn.close()

        
    return render_template('form_habitacion_cama.html')




@main.route('/dashboard/historico')
def dashboard_historico():
    asistente = request.args.get('asistente')
    rango_fecha = request.args.get('rango_fecha') or "24h"
    estado = request.args.get('estado')
    habitacion = request.args.get('habitacion')
    cama = request.args.get('cama')
    conn = get_db_connection()
    try:
        historico = get_historico_completo(conn, asistente, rango_fecha, estado, habitacion, cama)
        llamadas = historico['mensaje'] if historico['exito'] else []
        return render_template('historico.html', llamadas=llamadas)
    finally:
        conn.close()

@main.route('/llamada/<int:habitacion>/<string:cama>', methods=['GET'])
def llamada(habitacion, cama):
    conn = get_db_connection()
    try:
        existe_llamada = get_existe_llamada(conn, habitacion, cama)
        # se realiza consulta con exito
        if existe_llamada['exito']: 
            # no existe llamada  
            if not existe_llamada['mensaje']:
                id_cama = get_id_cama(conn, habitacion, cama)
                # se procede a crear llamda    
                salida = crear_llamada(conn, id_cama)
                # se ha creado la llamada con exito
                if salida['exito']:
                    enviar_notificacion_llamada(habitacion, cama)
                    _logging.info('LLAMADA REALIZADA')
                    return jsonify({'mensaje': salida['mensaje']}), 200
                # error al crear la llamada
                else:
                    _logging.info('ERROR...NO SE HA REALIZADO LA LLAMADA')
                    return jsonify({"mensaje": salida}), 500
            _logging.info('Ya existe una llamada activa para esa cama')
            return jsonify({'mensaje': 'Ya existe una llamada activa para esa cama'}), 409
        # error en la conexion 
        else:
            _logging.info('ERROR...ERROR EN LA BASE DE DATOS')
            return jsonify({'status': 'error', 'mensaje': 'Error al consultar la base de datos'}), 500
    finally:
        conn.close()

@main.route('/presencia/<int:habitacion>/<string:cama>', methods=['GET'])
def presencia(habitacion, cama):
  
    conn = get_db_connection()
    try:
        id_llamada = get_id_llamada_aceptada(conn,habitacion, cama)
        salida = nueva_presencia(conn, id_llamada)
        if salida['exito']:
            try:
                requests.get(f'http://localhost:5000/lampara/{habitacion}/{cama}/off')
            except Exception as e:
                _logging.error(f'Error encendiendo lámpara: {e}') 
            return jsonify({'mensaje': salida['mensaje']}), 200
        return jsonify({'mensaje': salida['mensaje']}), 400
    except Exception as e:
        _logging.error(f"Error en presencia: {e}")
        return jsonify({'status': 'error', 'mensaje': str(e)}), 500
    finally:
        conn.close()


@main.route('/llamada/atendida')
def atendida():
    habitacion = request.args.get('habitacion')
    cama = request.args.get('cama')
    nombre = request.cookies.get('nombre_asistente')
    codigo = request.cookies.get('codigo_acceso_asistente')
    _logging.debug(f"Cookies recibidas: nombre={nombre}, codigo={codigo}")
    conn = get_db_connection()
    try:
        id_llamada = get_id_llamada(conn, habitacion, cama)
        if not id_llamada:
            return jsonify({'mensaje': f'Llamada ya fue atendida por otra persona'}), 409
        asistente = get_asistente(conn, nombre, codigo)
        id_asistente = asistente['mensaje']['id']
        salida = llamada_atendida(conn, id_asistente, id_llamada)
        if salida:
            try:
                requests.get(f'http://localhost:5000/lampara/{habitacion}/{cama}/on')
            except Exception as e:
                _logging.error(f'Error encendiendo lámpara: {e}')            
            return jsonify({'mensaje': f'Llamada atendida por ti'}), 200
       
    finally:
        conn.close()

@main.route('/lampara/<int:habitacion>/<string:cama>/on', methods=['GET'])
def lampara_on(habitacion, cama):
    conn = get_db_connection()
    try:
        id_cama = get_id_cama(conn, habitacion, cama)
        if id_cama:
            cursor = conn.cursor()
            cursor.execute("UPDATE cama SET lampara=1 WHERE id=%s", (id_cama,))
            conn.commit()
            cursor.close()
            return jsonify({"mensaje": "Lámpara encendida"}), 200
        return jsonify({"mensaje": "No se encontró la cama"}), 404
    finally:
        conn.close()

@main.route('/lampara/<int:habitacion>/<string:cama>/off', methods=['GET'])
def lampara_off(habitacion, cama):
    conn = get_db_connection()
    try:
        id_cama = get_id_cama(conn, habitacion, cama)
        if id_cama:
            cursor = conn.cursor()
            cursor.execute("UPDATE cama SET lampara=0 WHERE id=%s", (id_cama,))
            conn.commit()
            cursor.close()
            return jsonify({"mensaje": "Lámpara apagada"}), 200
        return jsonify({"mensaje": "No se encontró la cama"}), 404
    finally:
        conn.close()

@main.route('/asistencias')
def asistencias():
    conn = get_db_connection()
    try:
        historico = get_historico_completo(conn, None, '24h', None)
        llamadas = historico['mensaje'] if historico['exito'] else []
        return render_template('asistencias.html', llamadas=llamadas)
    finally:
        conn.close()
