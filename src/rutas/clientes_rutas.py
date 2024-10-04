from flask import request, redirect, url_for, flash, render_template, jsonify
from models import SessionLocal
from models.clientes import Clientes

# Función para registrar las rutas en la aplicación Flask
def registrar_rutas(app):
    # Ruta para mostrar el formulario de creación de cliente (GET)
    @app.route('/clientes_crear', methods=['GET'])
    def mostrar_formulario_crear_cliente():
        return render_template('form_crear_cliente.html', titulo_pagina="Crear cliente")

    # Ruta para recibir los datos del formulario y crear un cliente (POST)
    @app.route('/clientes_crear', methods=['POST'])
    def crear_cliente():
        db = SessionLocal()
        tipo_documento = request.form['tipoDocumento']
        numero_documento = request.form['numeroDocumento']
        nombre = request.form['nombreCliente']
        apellido = request.form['apellidoCliente']
        telefono = request.form['telefonoCliente']
        direccion = request.form['direccionCliente']
        email = request.form['emailCliente']

        nuevo_cliente = Clientes(
            tipo_documento=tipo_documento,
            numero_documento=numero_documento,
            nombre=nombre,
            apellido=apellido,
            telefono=telefono,
            direccion=direccion,
            email=email,
            is_active=True
        )

        try:
            db.add(nuevo_cliente)
            db.commit()
            flash('Cliente creado con éxito', 'success')
        except Exception as e:
            db.rollback()
            flash(f'Error al crear cliente: {str(e)}', 'danger')
        finally:
            db.close()

        return redirect(url_for('mostrar_formulario_crear_cliente'))

    # Ruta para ver todos los clientes
    @app.route('/clientes_ver', methods=['GET'])
    def ver_clientes():
        db = SessionLocal()
        clientes = db.query(Clientes).filter_by(is_deleted=False).all()
        db.close()
        return render_template('form_ver_cliente.html', titulo_pagina="Ver Clientes", clientes=clientes)

    # Ruta para mostrar el formulario de edición (GET)
    @app.route('/clientes_editar', methods=['GET'])
    def mostrar_formulario_editar_cliente():
        return render_template('form_editar_cliente.html', titulo_pagina="Editar Cliente")

    # Ruta para buscar un cliente por documento
    @app.route('/clientes_buscar', methods=['GET'])
    def buscar_cliente():
        tipo_documento = request.args.get('tipoDocumento')
        numero_documento = request.args.get('numeroDocumento')
        db = SessionLocal()
        cliente = db.query(Clientes).filter_by(tipo_documento=tipo_documento, numero_documento=numero_documento).first()
        db.close()
        if cliente:
            return jsonify({
                'id': cliente.id,
                'tipo_documento': cliente.tipo_documento,
                'numero_documento': cliente.numero_documento,
                'nombre': cliente.nombre,
                'apellido': cliente.apellido,
                'telefono': cliente.telefono,
                'direccion': cliente.direccion,
                'email': cliente.email,
                'is_active': cliente.is_active
            })
        else:
            return jsonify({'error': 'Cliente no encontrado'}), 404

    # Ruta para actualizar un cliente (POST)
    @app.route('/clientes_actualizar', methods=['POST'])
    def actualizar_cliente():
        db = SessionLocal()
        cliente_id = request.form['clienteId']
        tipo_documento = request.form['tipoDocumento']
        numero_documento = request.form['cedulaCliente']
        nombre = request.form['nombreCliente']
        apellido = request.form['apellidoCliente']
        telefono = request.form['telefonoCliente']
        direccion = request.form['direccionCliente']
        email = request.form['emailCliente']
        estado_cliente = request.form['estadoCliente']

        cliente = db.query(Clientes).filter_by(id=cliente_id).first()

        if cliente:
            cliente.tipo_documento = tipo_documento
            cliente.numero_documento = numero_documento
            cliente.nombre = nombre
            cliente.apellido = apellido
            cliente.telefono = telefono
            cliente.direccion = direccion
            cliente.email = email
            cliente.is_active = estado_cliente.lower() == 'activo'

            try:
                db.commit()
                flash('Cambios guardados correctamente', 'success')
            except Exception as e:
                db.rollback()
                flash(f'Error al guardar los cambios: {str(e)}', 'danger')
        else:
            flash('Cliente no encontrado', 'danger')

        db.close()
        return redirect(url_for('mostrar_formulario_editar_cliente', cliente_id=cliente_id))

    # Ruta para eliminar cliente (lógica)
    @app.route('/clientes_eliminar', methods=['POST'])
    def eliminar_cliente():
        data = request.get_json()
        numero_documento = data.get('numeroDocumento')
        tipo_documento = data.get('tipoDocumento')
        db = SessionLocal()
        cliente = db.query(Clientes).filter_by(numero_documento=numero_documento, tipo_documento=tipo_documento).first()

        if cliente and not cliente.is_deleted:
            cliente.is_deleted = True

            try:
                db.commit()
                return jsonify({'success': True, 'message': 'Cliente eliminado correctamente.'})
            except Exception as e:
                db.rollback()
                return jsonify({'success': False, 'message': f'Error al eliminar el cliente: {str(e)}'})
        else:
            return jsonify({'success': False, 'message': 'Cliente no encontrado o ya eliminado.'}), 404
        db.close()
