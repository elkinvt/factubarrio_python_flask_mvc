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
        nombres_cliente = request.form['nombreCliente']
        telefono = request.form['telefonoCliente']
        direccion = request.form['direccionCliente']  # Aquí se recibe la dirección como texto
        email = request.form['emailCliente']

        # Crear el cliente con la dirección en texto
        nuevo_cliente = Clientes(
            tipo_documento=tipo_documento,
            numero_documento=numero_documento,
            nombres_cliente=nombres_cliente,
            telefono=telefono,
            direccion=direccion,  # Ahora la dirección se almacena directamente como texto
            email=email,
            is_active=True,
            is_deleted=False
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
        tipo_documento = request.args.get('tipoDocumento')
        numero_documento = request.args.get('numeroDocumento')

        # Verificar si se ingresan ambos campos
        if not tipo_documento or not numero_documento:
            return render_template('form_editar_cliente.html', mensaje="Faltan datos para la búsqueda", cliente=None, titulo_pagina="Editar Cliente")

        db = SessionLocal()
        cliente = db.query(Clientes).filter_by(
            tipo_documento=tipo_documento,
            numero_documento=numero_documento,
            is_deleted=False
        ).first()
        db.close()

        if cliente:
            return render_template('form_editar_cliente.html', cliente=cliente, titulo_pagina="Editar Cliente")
        else:
            # Si no se encuentra el cliente, pasamos el mensaje de error
            return render_template('form_editar_cliente.html', mensaje="Cliente no encontrado", cliente=None, titulo_pagina="Editar Cliente")

    # Ruta para buscar un cliente por documento
    @app.route('/clientes_buscar', methods=['GET'])
    def buscar_cliente():
        tipo_documento = request.args.get('tipoDocumento')
        numero_documento = request.args.get('numeroDocumento')

        # Verificar si se ingresan ambos campos
        if not tipo_documento or not numero_documento:
            return render_template('error.html', mensaje="Faltan datos para la búsqueda")

        db = SessionLocal()
        cliente = db.query(Clientes).filter_by(
            tipo_documento=tipo_documento,
            numero_documento=numero_documento,
            is_deleted=False  # Aseguramos que el cliente no esté marcado como eliminado
        ).first()
        db.close()

        if cliente:
            # Renderizar la plantilla de edición con los datos del cliente
            return render_template('form_editar_cliente.html', cliente=cliente, titulo_pagina=f"Editar Cliente")
        else:
            return render_template('form_editar_cliente.html', mensaje="Cliente no encontrado", cliente=None)

        
        
   


    # Ruta para actualizar un cliente (POST)
    @app.route('/clientes_actualizar', methods=['POST'])
    def actualizar_cliente():
        db = SessionLocal()
        cliente_id = request.form['clienteId']
        tipo_documento = request.form['tipoDocumento']
        numero_documento = request.form['numeroDocumento']  # Corregido
        nombres_cliente = request.form['nombreCliente']  # Corrección: eliminar la coma al final
        telefono = request.form['telefonoCliente']
        direccion = request.form['direccionCliente']
        email = request.form['emailCliente']
        estado_cliente = request.form['estadoCliente']

        # Buscar cliente por idclientes, que es el nombre correcto del campo
        cliente = db.query(Clientes).filter_by(idclientes=cliente_id).first()

        if cliente:
            # Actualizamos los campos del cliente
            cliente.tipo_documento = tipo_documento
            cliente.numero_documento = numero_documento
            cliente.nombres_cliente = nombres_cliente
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
        # Redirigir a la página de edición del cliente
        return redirect(url_for('mostrar_formulario_editar_cliente', cliente_id=cliente_id))

    
    
    
    
    # Ruta para activar o desactivar un Cliente
    @app.route('/clientes_toggle_estado', methods=['POST'])
    def toggle_estado_cliente():
        db = SessionLocal()
        numero_documento = request.form['numeroDocumento']
        tipo_documento = request.form['tipoDocumento']

        try:
            cliente = db.query(Clientes).filter_by(numero_documento=numero_documento, tipo_documento=tipo_documento).first()
            if cliente:
                cliente.is_active = not cliente.is_active
                db.commit()
                estado = 'activado' if cliente.is_active else 'desactivado'
                flash(f'Cliente {estado} con éxito.', 'success')
            else:
                flash('Cliente no encontrado.', 'danger')
        except Exception as e:
            db.rollback()
            flash(f'Error al cambiar el estado del cliente: {str(e)}', 'danger')
        finally:
            db.close()

        return redirect(url_for('ver_clientes'))
    
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
