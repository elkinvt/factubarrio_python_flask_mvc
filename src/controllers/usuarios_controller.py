from src.app import app 
from flask import render_template, request, url_for, flash,redirect, jsonify
from flask_controller import FlaskController
from src.models.usuarios import Usuarios  
from src.models import db_session_manager

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

            flash("Usuario creado exitosamente",'success')
            return redirect(url_for('usuarios_ver'))
        
        # Si el método es GET, simplemente renderiza el formulario
        return render_template('form_crear_usuario.html', titulo_pagina="Crear usuario")
    
    #-------------

    # Ruta para mostrar el formulario de edición de usuario (GET)
    @app.route('/usuarios_editar', methods=['GET'])
    def usuarios_editar():
        nombre_usuario = request.args.get('nombre')  # Obtener el nombre del usuario desde los parámetros de la URL

        if not nombre_usuario:
            flash('Por favor, proporcione el nombre del usuario.', 'warning')
            return render_template('form_editar_usuario.html', usuario=None, titulo_pagina="Editar Usuario")

        try:
            # Llamar al método del modelo para buscar el usuario por nombre sin manejar la sesión
            usuario = Usuarios.buscar_usuario_por_nombre(nombre_usuario)
            
            if usuario:
                if usuario['is_deleted']:
                    flash('Este usuario ha sido eliminado y no puede ser editado.', 'danger')
                    return render_template('form_editar_usuario.html', usuario=None, titulo_pagina="Usuario Eliminado")
                
                return render_template('form_editar_usuario.html', usuario=usuario, titulo_pagina="Editar Usuario")
            else:
                flash('Usuario no encontrado. Verifique el nombre proporcionado.', 'danger')
                return render_template('form_editar_usuario.html', usuario=None, titulo_pagina="Editar Usuario")
            
        except Exception as e:
            flash(f'Error al buscar el usuario: {str(e)}', 'danger')
            return render_template('form_editar_usuario.html', usuario=None, titulo_pagina="Error al Editar Usuario")
    #--------

    # Ruta para actualizar un usuario (POST)
    @app.route('/usuarios_actualizar', methods=['POST'])
    def actualizar_usuarios():

    
        usuario_id = request.form['usuarioId']
        nombre_usuario = request.form['nombreUsuario'].title()
        email = request.form['emailUsuario']
        rol = request.form['rolUsuario']
        is_active = request.form['estadousuario'].lower() == 'activo'
        nueva_contraseña = request.form.get('nuevaContraseña')
        confirmar_contraseña = request.form.get('confirmarContraseña')


        # Diccionario de datos actualizados
        datos_actualizados = {
            'nombres_usuario': nombre_usuario,
            'email': email,
            'rol': rol,
            'is_active': is_active
        }

        # Verificar si se ingresó una nueva contraseña y si coincide con la confirmación
        if nueva_contraseña:
            if nueva_contraseña == confirmar_contraseña:
                datos_actualizados['contraseña'] = nueva_contraseña  # Almacena la contraseña sin encriptar por ahora
            else:
                flash('Las contraseñas no coinciden.', 'danger')
                return redirect(url_for('usuarios_editar'))  # Redirigir en caso de error

        try:
            Usuarios.actualizar_usuario(usuario_id, datos_actualizados)
            flash('Cambios guardados correctamente.', 'success')
        except ValueError:
            flash('Usuario no encontrado.', 'danger')
        except Exception as e:
            flash(f'Error al guardar los cambios: {str(e)}', 'danger')

        return redirect(url_for('usuarios_ver'))

        
    #--------------------

    # Ruta para verificar el email del usuario
    @app.route('/usuarios/verificar_email', methods=['GET'])
    def verificar_email():
        email = request.args.get('email')
        with db_session_manager() as session:
            usuario_existente = session.query(Usuarios).filter_by(email=email).first()
            return jsonify({'exists': usuario_existente is not None})
        
    #---------
    # Ruta para actualizar el estado de un usuario
    @app.route('/usuario_toggle_estado', methods=['POST'])
    def toggle_estado_usuario():
        nombres_usuario = request.form['nombreUsuario']
        

        nuevo_estado = Usuarios.actualizar_estado(nombres_usuario)

        if nuevo_estado is not None:
            flash(f'Usuario {"activado" if nuevo_estado else "desactivado"} con éxito.', 'success')
        else:
            flash('Usuario no encontrado.', 'danger')

        return redirect(url_for('usuarios_editar', nombre=nombres_usuario))

    #----------

    # Ruta para eliminar usuario (lógica)
    @app.route('/usuario_eliminar', methods=['POST'])
    def eliminar_usuario():
        nombres_usuario = request.form.get('nombreUsuario')

        if not nombres_usuario:
            flash('Error: Nombre de usuario no proporcionado.', 'danger')
            return redirect(url_for('usuarios_ver'))

        try:

            if Usuarios.eliminar_usuario_logicamente(nombres_usuario):
                flash('usuario eliminado correctamente.', 'success')
            else:
                flash('usuario no encontrado o ya eliminado.', 'danger')
        except Exception as e:
            flash(f'Error al eliminar el usuario: {str(e)}', 'danger')

        return redirect(url_for('usuarios_ver'))


    #-----------