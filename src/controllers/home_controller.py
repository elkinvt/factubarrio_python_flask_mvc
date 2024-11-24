from src.app import app 
from flask import render_template, flash,redirect,url_for,session
from flask_controller import FlaskController

class Index_Controller(FlaskController):
    @app.route('/Index')
    def Index():
        # Verificar si el usuario ha iniciado sesión
        if 'usuario_id' not in session:  # Cambia 'usuario_id' por el identificador que uses para la sesión
            flash("Debe iniciar sesión para acceder a las funcionalidades del sistema.", "warning")
            return redirect(url_for('login'))  # Redirige a la página de login
        return render_template('index.html', titulo_pagina ="Inicio")
