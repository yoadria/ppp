from flask import Blueprint, render_template, jsonify, request
from database.conexion import get_db_connection
from database.insertar_datos import *
from .pushover_app import enviar_notificacion_llamada

main = Blueprint('main', __name__)

# ruta de inicio
@main.route('/')
def index():
    return render_template('index.html')

@main.route('/panel_habitacion')
def panel_habitacion():
    return render_template('panelhab.html')


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
    
@main.route('/api/llamada', methods=['POST'])
def crear_llamada():
    data = request.get_json()


@main.route('/llamada/<int:habitacion>/<string:cama>', methods=['GET'])
def llamada(habitacion, cama):
    enviar_notificacion_llamada(habitacion, cama)
    return jsonify({'status': 'ok', 'mensaje': f'Llamada registrada para habitación {habitacion}, cama {cama}'}), 200