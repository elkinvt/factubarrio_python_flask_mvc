from src.app import app
from flask_controller import FlaskController
from flask import request, redirect, url_for, flash, render_template, jsonify
from src.models.clientes import Clientes

class Clientes_Controller(FlaskController):
    
    # Ruta para ver todos los clientes
    @app.route('/clientes_ver', methods=['GET'])
    def clientes_ver():
        clientes = Clientes.obtener_clientes()
        return render_template('form_ver_cliente.html', titulo_pagina="Ver Clientes", clientes=clientes)

    #----------------------------------

    # Ruta para crear el cliente
    @app.route('/clientes_crear', methods=['GET', 'POST'])
    def clientes_crear():
        if request.method == 'GET':
            return render_template('form_crear_cliente.html', titulo_pagina="Crear Cliente")
        
        if request.method == 'POST':
            tipo_documento = request.form['tipoDocumento']
            numero_documento = request.form['numeroDocumento']
            nombre_completo = request.form['nombreCliente'].title()
            telefono = request.form['telefonoCliente']
            direccion = request.form['direccionCliente']
            email = request.form['emailCliente']

            # Validaciones y mensajes de error
            errores = {}
            if not tipo_documento:
                errores['tipoDocumento'] = 'El tipo de documento es obligatorio.'
            if not numero_documento:
                errores['numeroDocumento'] = 'El número de documento es obligatorio.'
            elif not numero_documento.isdigit():
                errores['numeroDocumento'] = 'Debe contener solo números.'
            elif len(numero_documento) < 6 or len(numero_documento) > 15:
                errores['numeroDocumento'] = 'Debe tener entre 6 y 15 dígitos.'
            
            if not nombre_completo:
                errores['nombreCliente'] = 'El nombre es obligatorio.'
            elif len(nombre_completo) < 3 or len(nombre_completo) > 50:
                errores['nombreCliente'] = 'Debe tener entre 3 y 50 caracteres.'

            if not telefono:
                errores['telefonoCliente'] = 'El teléfono es obligatorio.'
            elif not telefono.isdigit():
                errores['telefonoCliente'] = 'Debe contener solo números.'
            elif len(telefono) < 10:
                errores['telefonoCliente'] = 'Debe tener al menos 10 dígitos.'

            if not direccion:
                errores['direccionCliente'] = 'La dirección es obligatoria.'
            elif len(direccion) < 10:
                errores['direccionCliente'] = 'Debe tener al menos 10 caracteres.'

            if not email:
                errores['emailCliente'] = 'El email es obligatorio.'
            elif "@" not in email or "." not in email.split("@")[-1]:
                errores['emailCliente'] = 'Debe ser un email válido.'

            # Validación de duplicados
            duplicados = Clientes.validar_datos(numero_documento=numero_documento, email=email)
            if duplicados:
                errores.update(duplicados)

            # Si hay errores, devolvemos JSON con errores
            if errores:
                return jsonify({'status': 'error', 'errores': errores}), 400

            # Si todas las validaciones pasan, intentamos crear el cliente
            nuevo_cliente = Clientes(
                tipo_documento=tipo_documento,
                numero_documento=numero_documento,
                nombres_cliente=nombre_completo,
                telefono=telefono,
                direccion=direccion,
                email=email,
                is_active=True,
                is_deleted=False
            )

            try:
                Clientes.agregar_cliente(nuevo_cliente)
                return jsonify({'success': True, 'message': 'Cliente creado con éxito'}), 200
            except Exception as e:
                return jsonify({'success': False, 'message': f'Error al crear cliente: {str(e)}'}), 500


    #------------------------

    # Ruta para mostrar el formulario de edición (GET)  
    @app.route('/clientes_editar', methods=['GET'])
    def clientes_editar():
        tipo_documento = request.args.get('tipoDocumento')
        numero_documento = request.args.get('numeroDocumento')

        if not tipo_documento or not numero_documento:
            flash('Por favor, ingrese ambos campos: Tipo de Documento y Número de Documento.', 'warning')
            return render_template('form_editar_cliente.html', cliente=None, titulo_pagina="Editar Cliente")

        try:
            # Llamar al método del modelo para buscar el cliente sin manejar la sesión
            cliente = Clientes.buscar_cliente_por_documento(tipo_documento, numero_documento)
            
            if cliente:
                if cliente['is_deleted']:
                    flash('Este cliente ha sido eliminado y no puede ser editado.', 'danger')
                    return render_template('form_editar_cliente.html', cliente=None, titulo_pagina="Cliente Eliminado")
                return render_template('form_editar_cliente.html', cliente=cliente, titulo_pagina="Editar Cliente")
            else:
                flash('Cliente no encontrado. Verifique los datos ingresados.', 'danger')
                return render_template('form_editar_cliente.html', cliente=None, titulo_pagina="Editar Cliente")
            
        except Exception as e:
            flash(f'Error al buscar el cliente: {str(e)}', 'danger')
            return render_template('form_editar_cliente.html', cliente=None, titulo_pagina="Error al Editar cliente")

    #---------------------------------

    # Ruta para actualizar un cliente (POST)
    @app.route('/clientes_actualizar', methods=['POST'])
    def actualizar_cliente():
        cliente_id = request.form['clienteId']
        tipo_documento = request.form['tipoDocumento']
        numero_documento = request.form['numeroDocumento']
        nombre_completo = request.form['nombreCliente'].title()
        telefono = request.form['telefonoCliente']
        direccion = request.form['direccionCliente']
        email = request.form['emailCliente']
        is_active = request.form['estadoCliente'].lower() == 'activo'


        # Diccionario de errores específicos por campo
        errores = {}

        # Validaciones
        if not nombre_completo:
            errores['nombreCliente'] = 'El nombre es obligatorio.'
        elif len(nombre_completo) < 3 or len(nombre_completo) > 50:
            errores['nombreCliente'] = 'Debe tener entre 3 y 50 caracteres.'

        if not telefono:
            errores['telefonoCliente'] = 'El teléfono es obligatorio.'
        elif not telefono.isdigit():
            errores['telefonoCliente'] = 'Debe contener solo números.'
        elif len(telefono) < 10:
            errores['telefonoCliente'] = 'Debe tener al menos 10 dígitos.'

        if not direccion:
            errores['direccionCliente'] = 'La dirección es obligatoria.'
        elif len(direccion) < 10:
            errores['direccionCliente'] = 'Debe tener al menos 10 caracteres.'

        if not email:
            errores['emailCliente'] = 'El email es obligatorio.'
        elif "@" not in email or "." not in email.split("@")[-1]:
            errores['emailCliente'] = 'Debe ser un email válido.'

        # Validación de duplicados, excluyendo el cliente actual
        duplicados = Clientes.validar_datos(numero_documento=numero_documento, email=email, cliente_id=cliente_id)
        if duplicados:
            errores.update(duplicados)

        # Si hay errores, devolver un JSON con los errores
        if errores:
            return jsonify({'status': 'error', 'errores': errores}), 400

        # Diccionario de datos actualizados
        datos_actualizados = {
            'tipo_documento': tipo_documento,
            'numero_documento': numero_documento,
            'nombres_cliente': nombre_completo,
            'telefono': telefono,
            'direccion': direccion,
            'email': email,
            'estadoCliente': is_active
        }

        try:
            Clientes.actualizar_cliente(cliente_id, datos_actualizados)
            return jsonify({'success': True, 'message': 'Cliente actualizado con éxito'}), 200
        except Exception as e:
            return jsonify({'success': False, 'message': f'Error al actualizar cliente: {str(e)}'}), 500

        
    #--------------------

    
    # Ruta para actualizar el estado de un cliente
    @app.route('/clientes_toggle_estado', methods=['POST'])
    def toggle_estado_cliente():
        tipo_documento = request.form['tipoDocumento']
        numero_documento = request.form['numeroDocumento']

        nuevo_estado = Clientes.actualizar_estado(tipo_documento, numero_documento)

        if nuevo_estado is not None:
            flash(f'Cliente {"activado" if nuevo_estado else "desactivado"} con éxito.', 'success')
        else:
            flash('Cliente no encontrado.', 'danger')

        return redirect(url_for('clientes_editar', tipoDocumento=tipo_documento, numeroDocumento=numero_documento))

    #----------

    # Ruta para eliminar cliente (lógica)
    @app.route('/clientes_eliminar', methods=['POST'])
    def eliminar_cliente():
        tipo_documento = request.form.get('tipoDocumento')
        numero_documento = request.form.get('numeroDocumento')

        try:

            if Clientes.eliminar_cliente_logicamente(tipo_documento, numero_documento):
                flash('Cliente eliminado correctamente.', 'success')
            else:
                flash('Cliente no encontrado o ya eliminado.', 'danger')
        except Exception as e:
            flash(f'Error al eliminar el cliente: {str(e)}', 'danger')

        return redirect(url_for('clientes_ver'))


    #-----------

    # Ruta para buscar cliente por numero de documento
    @app.route('/buscar_clientes_por_numero_documento')
    def buscar_clientes_por_numero_documento():
        query = request.args.get('q', '')
        clientes_data = Clientes.buscar_por_numero_documento(query)
        return jsonify(clientes_data)

    #------------------

    # Ruta para validar los datos de un cliente
    @app.route('/validar_cliente', methods=['POST'])
    def validar_cliente():
        data = request.get_json()
        errores = Clientes.validar_datos(
            numero_documento=data.get('numeroDocumento'),
            email=data.get('emailCliente')
        )
        if errores:
            return jsonify({'status': 'error', 'errores': errores}), 400
        return jsonify({'status': 'success'})
    
    #---------------------


    
