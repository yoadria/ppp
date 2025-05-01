from flask import Flask, jsonify, request, send_from_directory
import logging
from database.conexion import get_db_connection
from database.tablas_db import crear_tabla_llamadas
_logging = logging.getLogger(__name__)
from app import create_app
app = create_app()


if __name__ == '__main__':
    app.run(debug = True, host="0.0.0.0") #Que no sea visible para todo el mundo - para eso usar un host ="0.0.0.0"