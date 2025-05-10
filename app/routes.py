from flask import Blueprint, render_template, jsonify, request
from database.conexion import get_db_connection
from database.insertar_datos import *
from database.solicitar_datos import *
from .pushover_app import *
from database.actualizar_datos import *
import logging


logging.basicConfig(
    level=logging.DEBUG,  # Muestra los logs de nivel DEBUG y superior
    format='%(asctime)s - %(levelname)s - %(message)s'  # Formato para mostrar los logs
)

_logging = logging.getLogger(__name__)
main = Blueprint('main', __name__)

# ruta de inicio
@main.route('/')
def index():
    return render_template('index.html')

@main.route('/panel_habitacion')
def panel_habitacion():
    #import wdb; wdb.set_trace()
    conn = get_db_connection()
    lampara = get_lampara(conn, '101A')
    return render_template('panelhab.html', lampara=lampara)


# ruta para crear asistente post
@main.route('/api/asistente', methods=['POST'])
def crear_asistente():
    data = request.get_json()
    nombre = data.get('nombre')
    codigo_acceso = data.get('codigo_acceso')
    

    if not nombre or not codigo_acceso:
        return jsonify({"mensaje": "Faltan datos"}), 400

   
    datos = {'nombre': nombre, 'codigo':codigo_acceso}
    conn = get_db_connection()
    salida = nuevo_asistente(conn, datos)

    if salida['exito']:
       
        return jsonify({"mensaje": salida}), 201
    else:
       
        return jsonify({"mensaje": salida}), 500
    
@main.route('/formulario/asistente')
def formulario_asistente():
    return render_template('form_asistente.html')

@main.route('/formulario/habitacion')
def formulario_habitacion():
    return render_template('form_habitacion_cama.html')

@main.route('/dashboard/historico')
def dashboard_historico():
    return render_template('historico.html')

# ruta para crear habitacion post    
@main.route('/api/habitacion', methods=['POST'])
def crear_habitacion():
    data = request.get_json()
    numero = data.get('numero')
    planta = data.get('planta')

    if not numero or not planta:
        return jsonify({"mensaje": "Faltan datos"}), 400

    datos = {'numero': numero, 'planta':planta}
    conn = get_db_connection()
    salida = nueva_habitacion(conn, datos)

    if salida['exito']:
        
        return jsonify({"mensaje": salida}), 201
    else:
       
        return jsonify({"mensaje": salida}), 500
    

# ruta para crear cama post    
@main.route('/api/cama', methods=['POST'])
def crear_cama():
    data = request.get_json()
    codigo = data.get('codigo')
    id_habitacion = data.get('id_habitacion')

    if not codigo or not id_habitacion:
        return jsonify({"mensaje": "Faltan datos"}), 400

    
    datos = {'codigo': codigo, 'id_habitacion':id_habitacion}
    conn = get_db_connection()
    salida = nueva_cama(conn, datos)

    if salida['exito']:
       
        return jsonify({"mensaje": salida}), 201
    else:
        
        return jsonify({"mensaje": salida}), 500
    


@main.route('/llamada/<int:habitacion>/<string:cama>', methods=['GET'])
def llamada(habitacion, cama):
    # import wdb; wdb.set_trace()
    conn = get_db_connection()
    existe_llamada = get_existe_llamada(conn, cama)

    # se realiza consulta con exito
    if existe_llamada['exito']: 

        # hay una llamada activa no hace nada   
        if existe_llamada['mensaje'] != None:
            # return jsonify({'status': 'ok', 'mensaje': f'Llamada ya registrada para habitación {habitacion}, cama {cama}'}), 200
            _logging.debug("hay una llamada en espera")
            return jsonify({'status': 'ok', 'mensaje': f'ya hay una llamada realizada'}), 200

        #no existe la llamada
        else:
            _logging.info("No hay llamada en espera")
            # se procede a crear llamda    
            salida = crear_llamada(conn, cama)
            # se a creado la llamada con exito
            if salida['exito']:
                receipt_id = enviar_notificacion_llamada(habitacion, cama)
                salida_actualizar = actualizar_receip_llamada(conn, cama, receipt_id)
                _logging.debug(salida_actualizar)

                _logging.debug("ID de respuesta: %s", receipt_id)
                return jsonify({'mensaje': salida}), 200
            #error al crear la llamda
            else:
                return jsonify({"mensaje": salida}), 500
    # error en  la conexion 
    else:
        return jsonify({'status': 'error', 'mensaje': 'Error al consultar la base de datos'}), 500


@main.route('/presencia/<int:habitacion>/<string:cama>', methods=['GET'])
def presencia(habitacion, cama):
    conn = get_db_connection()
    existe_llamada = get_existe_llamada(conn, cama)
    # se realiza consulta con exito
    if existe_llamada['exito']: 
        # hay una llamada activa no hace nada   
        if existe_llamada['mensaje'] != None:
            # import wdb; wdb.set_trace()
            _logging.debug("hay llamada en espera se procede a cerrar")
            receip_id = existe_llamada['mensaje']['receip_id']
            codigo_asistente = callback_pushover(receip_id)
            id_asistente = get_id_asistente(conn, codigo_asistente); id_asistente = id_asistente['mensaje']['id']
            datos_presencia = {'id_llamada': existe_llamada['mensaje']['id'], 'id_asistente': id_asistente}
            salida = nueva_presencia(conn, datos_presencia)
            if salida['exito']:
                _logging.debug("se ha cerrado la llamada")
                return jsonify({'status': 'ok', 'mensaje': f'Llamada cerrada para habitación {habitacion}, cama {cama}'}), 200
            else:
                return jsonify({"mensaje": salida['mensaje']}), 500
