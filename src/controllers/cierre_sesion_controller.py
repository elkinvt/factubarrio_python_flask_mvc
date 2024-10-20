from src.app import app 
from flask import render_template
from flask_controller import FlaskController

class Cerra_sesion_Controller(FlaskController):
    @app.route('/cerrar_sesion')
    def cerrar_sesion():
        return render_template('index.html')