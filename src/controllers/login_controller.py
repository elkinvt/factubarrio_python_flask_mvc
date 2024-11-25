from src.app import app 
from flask import render_template, request, redirect, url_for,flash, session
from flask_controller import FlaskController
from src.models.usuarios import Usuarios
from flask_login import login_user
class LoginController(FlaskController):
    @app.route('/', methods=['GET'])
    def home():
        return redirect(url_for('login'))

    @app.route('/login', methods=['POST','GET'])
    def login():    
        if request.method == 'POST':
            nombre_usuario = request.form.get('nombre_usuario')                
            contraseña = request.form.get('contraseña')    
            usuario_valido = Usuarios.validar_usuario_login(nombre_usuario, contraseña)
            if usuario_valido:
                login_user(usuario_valido)
                # Guardar el ID del usuario en la sesión
                session['usuario_id'] = usuario_valido.id_usuario  # Asegúrate de que `id_usuario` es el campo correcto
                return redirect(url_for('Index'))
            else:
                flash('Nombre de usuario o contraseña incorrectos',  'danger')
                return redirect(url_for('login'))
            
        return render_template('login.html', titulo_pagina = 'Login')