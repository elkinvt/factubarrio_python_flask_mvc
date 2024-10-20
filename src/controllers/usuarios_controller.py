from src.app import app 
from flask import render_template
from flask_controller import FlaskController

class Usuarios_Controller(FlaskController):
    
    @app.route('/usuarios_crear')
    def usuarios_crear():
        return render_template('form_crear_usuario.html', titulo_pagina = "Crear usuario")

    @app.route('/usuarios_ver')
    def usuarios_ver():
        return render_template('form_ver_usuario.html', titulo_pagina = "Ver usuario")

    @app.route('/usuarios_editar')
    def usuarios_editar():
        return render_template('form_editar_usuario.html', titulo_pagina = "Editar usuario")