from src.app import app 
from flask import render_template, request, url_for, flash,redirect
from flask_controller import FlaskController
from src.models.usuarios import Usuarios  

class Usuarios_Controller(FlaskController):

    # Ruta para ver todos los usuarios
    @app.route('/usuarios_ver', methods=['GET'])
    def usuarios_ver():
        usuarios = Usuarios.obtener_usuarios()
        return render_template('form_ver_usuario.html', titulo_pagina="Ver usurios", usuarios=usuarios)

    #--------------

    # Ruta para crear el usuario
    @app.route('/usuarios_crear', methods=['GET', 'POST'])
    def usuarios_crear():
        if request.method == 'POST':
            # Extrae los datos del formulario
            nombre = request.form.get('nombre'). title()
            email = request.form.get('email')
            contraseña = request.form.get('contraseña')
            rol = request.form.get('rol')

            # Crear el objeto usuario con los datos del formulario
            nuevo_usuario = Usuarios(
                nombre_usuario=nombre,
                email=email,
                contraseña=contraseña,
                rol=rol
            )

            # Llama al método agregar_usuario para guardar el usuario en la base de datos
            Usuarios.agregar_usuario(nuevo_usuario)

            flash("Usuario creado exitosamente")
            return redirect(url_for('usuarios_ver'))
        
        # Si el método es GET, simplemente renderiza el formulario
        return render_template('form_crear_usuario.html', titulo_pagina="Crear usuario")
    
    #-------------
    
    @app.route('/usuarios_editar')
    def usuarios_editar():
        return render_template('form_editar_usuario.html', titulo_pagina = "Editar usuario")