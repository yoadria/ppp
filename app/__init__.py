from flask import Flask
from database.conexion import init_db_connection

def create_app():
    app = Flask(__name__)

    # Inicializa la conexión global a la BD
    init_db_connection()
    

    from .routes import main
    app.register_blueprint(main)

    return app
