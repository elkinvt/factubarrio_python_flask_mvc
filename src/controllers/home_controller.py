from src.app import app 
from flask import render_template
from flask_controller import FlaskController

class Index_Controller(FlaskController):
    @app.route('/Index')
    def Index():
        return render_template('index.html', titulo_pagina ="INDEX")
