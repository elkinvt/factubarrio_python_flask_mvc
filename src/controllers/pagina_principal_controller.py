from src.app import app 
from flask import render_template
from flask_controller import FlaskController

class Pagina_principal_Controller(FlaskController):
    @app.route('/pagina_principal')
    def pagina_principal():
        return render_template('pgprincipal.html', titulo_pagina ="Pagina principal")
