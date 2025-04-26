from flask import Flask, jsonify, request
import logging
from database.conexion import get_db_connection
from database.tablas_db import crear_tabla_llamadas
_logging = logging.getLogger(__name__)

app = Flask(__name__)
@app.route('/')
def home():
    return "¡Hola desde Flask con Nginx!"
def inicio():
    conn = get_db_connection()
    if conn:
        crear_tabla_llamadas(conn)

if __name__ == '__main__':
    inicio()
    app.run(debug = True, host="0.0.0.0") #Que no sea visible para todo el mundo - para eso usar un host ="0.0.0.0"