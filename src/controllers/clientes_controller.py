from src.app import app
from flask_controller import FlaskController
from flask import request, redirect, url_for, flash, render_template, jsonify
from src.models.clientes import Clientes

class Clientes_Controller(FlaskController):
    
    # Ruta para ver todos los clientes
    @app.route('/clientes_ver', methods=['GET'])
    def ver_clientes():
        clientes = Clientes.obtener_clientes()
        return render_template('form_ver_cliente.html', titulo_pagina="Ver Clientes", clientes=clientes)

    #----------------------------------

    # Ruta para crear el cliente
    @app.route('/clientes_crear', methods=['GET', 'POST'])
    def crear_cliente():
        if request.method == 'GET':
            return render_template('form_crear_cliente.html', titulo_pagina="Crear Cliente")
        
        if request.method == 'POST':
            data = request.get_json()
            tipo_documento = data.get('tipoDocumento')
            numero_documento = data.get('numeroDocumento')
            nombres_cliente = data.get('nombreCliente').title()
            telefono = data.get('telefonoCliente')
            direccion = data.get('direccionCliente')
            email = data.get('emailCliente')

            errores = Clientes.validar_datos(numero_documento=numero_documento, email=email)
            if errores:
                return jsonify({'status': 'error', 'errores': errores}), 400

            nuevo_cliente = Clientes(
                tipo_documento=tipo_documento,
                numero_documento=numero_documento,
                nombres_cliente=nombres_cliente,
                telefono=telefono,
                direccion=direccion,
                email=email,
                is_active=True,
                is_deleted=False
            )

            with Clientes.session_scope() as db:
                Clientes.crear_o_actualizar(db, nuevo_cliente)
                return jsonify({'status': 'success', 'message': 'Cliente creado con éxito'}), 200

    #------------------------

    # Ruta para mostrar el formulario de edición (GET)  
    @app.route('/clientes_editar', methods=['GET'])
    def mostrar_formulario_editar_cliente():
        tipo_documento = request.args.get('tipoDocumento')
        numero_documento = request.args.get('numeroDocumento')

        if not tipo_documento or not numero_documento:
            flash('Por favor, ingrese ambos campos: Tipo de Documento y Número de Documento.', 'warning')
            return render_template('form_editar_cliente.html', cliente=None, titulo_pagina="Editar Cliente")

        # Utilizamos el método que devuelve un diccionario
        cliente = Clientes.buscar_cliente_como_diccionario(tipo_documento=tipo_documento, numero_documento=numero_documento)
        
        if cliente:
            if cliente['is_deleted']:
                flash('Este cliente ha sido eliminado y no puede ser editado.', 'danger')
                return render_template('form_editar_cliente.html', cliente=None, titulo_pagina="Cliente Eliminado")
            return render_template('form_editar_cliente.html', cliente=cliente, titulo_pagina="Editar Cliente")
        else:
            flash('Cliente no encontrado. Verifique los datos ingresados.', 'danger')
            return render_template('form_editar_cliente.html', cliente=None, titulo_pagina="Editar Cliente")

    #---------------------------------

    # Ruta para actualizar un cliente (POST)
    @app.route('/clientes_actualizar', methods=['POST'])
    def actualizar_cliente():
        cliente_id = request.form['clienteId']
        datos_actualizados = {
            'tipo_documento': request.form['tipoDocumento'],
            'numero_documento': request.form['numeroDocumento'],
            'nombres_cliente': request.form['nombreCliente'].title(),
            'telefono': request.form['telefonoCliente'],
            'direccion': request.form['direccionCliente'],
            'email': request.form['emailCliente'],
            'is_active': request.form['estadoCliente'].lower() == 'activo'
        }

        # Usamos el método que devuelve la instancia del modelo
        cliente = Clientes.buscar_cliente(idclientes=cliente_id)

        if cliente:
            with Clientes.session_scope() as db:
                Clientes.crear_o_actualizar(db, cliente, datos_actualizados)
                flash('Cambios guardados correctamente', 'success')
            return redirect(url_for('ver_clientes'))
        else:
            flash('Cliente no encontrado', 'danger')
            return redirect(url_for('mostrar_formulario_editar_cliente', tipoDocumento=datos_actualizados['tipo_documento'], numeroDocumento=datos_actualizados['numero_documento']))

    #--------------------

    # Ruta para actualizar el estado de un cliente
    @app.route('/clientes_toggle_estado', methods=['POST'])
    def toggle_estado_cliente():
        tipo_documento = request.form['tipoDocumento']
        numero_documento = request.form['numeroDocumento']

        with Clientes.session_scope() as db:
            # Recuperar el cliente en la misma sesión
            cliente = db.query(Clientes).filter_by(tipo_documento=tipo_documento, numero_documento=numero_documento).first()
            
            if cliente:
                cliente.is_active = not cliente.is_active  # Cambiar el estado directamente en la sesión activa
                db.add(cliente)  # Asegurarse de que el cliente esté adjunto a la sesión
                flash(f'Cliente {"activado" if cliente.is_active else "desactivado"} con éxito.', 'success')
            else:
                flash('Cliente no encontrado.', 'danger')

        return redirect(url_for('mostrar_formulario_editar_cliente', tipoDocumento=tipo_documento, numeroDocumento=numero_documento))

    #----------

    # Ruta para eliminar cliente (lógica)
    @app.route('/clientes_eliminar', methods=['POST'])
    def eliminar_cliente():
        tipo_documento = request.form.get('tipoDocumento')
        numero_documento = request.form.get('numeroDocumento')

        with Clientes.session_scope() as db:
            # Recuperar el cliente en la misma sesión
            cliente = db.query(Clientes).filter_by(tipo_documento=tipo_documento, numero_documento=numero_documento).first()

            if cliente and not cliente.is_deleted:
                cliente.is_deleted = True  # Marcamos el cliente como eliminado (eliminación lógica)
                db.add(cliente)  # Asegurarse de que el cliente esté adjunto a la sesión
                flash('Cliente eliminado correctamente.', 'success')
            else:
                flash('Cliente no encontrado o ya eliminado.', 'danger')

        return redirect(url_for('ver_clientes'))


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


    
