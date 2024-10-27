from src.app import app 
from flask_controller import FlaskController
from flask import request, redirect, url_for, flash, render_template, jsonify
from src.models import SessionLocal
from src.models.clientes import Clientes

class Clientes_Controller(FlaskController):
    
    # Ruta para ver todos los clientes
    @app.route('/clientes_ver', methods=['GET'])
    def ver_clientes():
        # Obtener los clientes desde el modelo Clientes
        clientes = Clientes.obtener_clientes()
        return render_template('form_ver_cliente.html', titulo_pagina="Ver Clientes", clientes=clientes)
    
    #----------------------------------

    
    # Ruta para crear el cliente
    @app.route('/clientes_crear', methods=['GET', 'POST'])
    def crear_cliente():
        if request.method == 'POST':
            # Procesar el formulario enviado
            db = SessionLocal()

            # Obtener los datos del formulario
            tipo_documento = request.form['tipoDocumento']
            numero_documento = request.form['numeroDocumento']
            nombres_cliente = request.form['nombreCliente'].title()
            telefono = request.form['telefonoCliente']
            direccion = request.form['direccionCliente']
            email = request.form['emailCliente']

            # Validar si hay datos duplicados antes de crear el cliente
            errores = Clientes.validar_datos(numero_documento=numero_documento, email=email)

            if errores:
                # Si hay errores de duplicados, mostrar un mensaje y no guardar
                for campo, mensaje in errores.items():
                    flash(f"{mensaje}", 'danger')
                return redirect(url_for('crear_cliente'))  # Redirige de vuelta al formulario

            # Si no hay duplicados, crear el cliente
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

            try:
                Clientes.agregar_cliente(db, nuevo_cliente) 
                flash('Cliente creado con éxito', 'success')
                return redirect(url_for('ver_clientes'))
            except Exception as e:
                db.rollback()  # Deshacer cambios si ocurre un error
                flash(f'Error al crear cliente: {str(e)}', 'danger')
            finally:
                db.close()

        # Si es GET, mostrar el formulario
        return render_template('form_crear_cliente.html', titulo_pagina="Crear Cliente")

    #------------------------
    
    # Ruta para mostrar el formulario de edición (GET)  
    @app.route('/clientes_editar', methods=['GET'])
    def mostrar_formulario_editar_cliente():
        tipo_documento = request.args.get('tipoDocumento')
        numero_documento = request.args.get('numeroDocumento')
        
         # Verificar si se ingresan ambos campos
        if not tipo_documento or not numero_documento:
            flash('Por favor, ingrese ambos campos: Tipo de Documento y Número de Documento.', 'warning')
            return render_template('form_editar_cliente.html', cliente=None, titulo_pagina="Editar Cliente")

        db = SessionLocal()  # Crear la sesión de base de datos
        try:
            # Usar la sesión en la función de búsqueda
            cliente = Clientes.buscar_cliente_por_documento(db, tipo_documento, numero_documento)

            if cliente:
                if cliente.is_deleted:
                    flash('Este cliente ha sido eliminado y no puede ser editado.', 'danger')
                    return render_template('form_editar_cliente.html', cliente=None, titulo_pagina="Cliente Eliminado")
                return render_template('form_editar_cliente.html', cliente=cliente, titulo_pagina="Editar Cliente")
            else:
                flash('Cliente no encontrado. Verifique los datos ingresados.', 'danger')
                return render_template('form_editar_cliente.html', cliente=None, titulo_pagina="Editar Cliente")
        except Exception as e:
            flash(f'Error al buscar el cliente: {str(e)}', 'danger')
        finally:
            db.close()  # Cerrar la sesión después de completar la operación
  
    #---------------------------------

    # Ruta para actualizar un cliente (POST)
    @app.route('/clientes_actualizar', methods=['POST'])
    def actualizar_cliente():
        cliente_id = request.form['clienteId']
        tipo_documento = request.form['tipoDocumento']
        numero_documento = request.form['numeroDocumento']
        nombres_cliente = request.form['nombreCliente'].title()
        telefono = request.form['telefonoCliente']
        direccion = request.form['direccionCliente']
        email = request.form['emailCliente']
        estado_cliente = request.form['estadoCliente'].lower() == 'activo'

        db = SessionLocal()
        cliente = Clientes.buscar_cliente_por_id(cliente_id)

        if cliente:
            # Diccionario de datos actualizados
            datos_actualizados = {
                'tipo_documento': tipo_documento,
                'numero_documento': numero_documento,
                'nombres_cliente': nombres_cliente,
                'telefono': telefono,
                'direccion': direccion,
                'email': email,
                'is_active': estado_cliente
            }

             # Verificar si el cliente está en la sesión actual, si no lo está, reasociarlo
            if not db.object_session(cliente):
                db.add(cliente)

            try:
                Clientes.actualizar_cliente(db, cliente, datos_actualizados)
                flash('Cambios guardados correctamente', 'success')
                return redirect(url_for('ver_clientes'))
            except Exception as e:
                flash(f'Error al guardar los cambios: {str(e)}', 'danger')
        else:
            flash('Cliente no encontrado', 'danger')

        db.close()
        return redirect(url_for('mostrar_formulario_editar_cliente', tipoDocumento=tipo_documento, numeroDocumento=numero_documento))
    
    #--------------------
    
    #ruta para actualizar el estado de un cliente
    @app.route('/clientes_toggle_estado', methods=['POST'])
    def toggle_estado_cliente():
        tipo_documento = request.form['tipoDocumento']
        numero_documento = request.form['numeroDocumento']
        
        db = SessionLocal()  # Crear una única sesión para toda la transacción
        try:
            # Usar la misma sesión para buscar al cliente y modificarlo
            cliente = Clientes.buscar_cliente_por_documento(db, tipo_documento, numero_documento)
            
            if cliente:
                Clientes.toggle_estado_cliente(db, cliente)  # Cambiar el estado y hacer commit en la misma sesión
                estado = 'activado' if cliente.is_active else 'desactivado'
                flash(f'Cliente {estado} con éxito.', 'success')
            else:
                flash('Cliente no encontrado.', 'danger')
        except Exception as e:
            db.rollback()  # Rollback si hay un error
            flash(f'Error al cambiar el estado del cliente: {str(e)}', 'danger')
        finally:
            db.close()  # Cierra la sesión después de hacer commit

        return redirect(url_for('mostrar_formulario_editar_cliente', tipoDocumento=tipo_documento, numeroDocumento=numero_documento))
    
    #----------
    
    # Ruta para eliminar cliente (lógica)
    @app.route('/clientes_eliminar', methods=['POST'])
    def eliminar_cliente():
        numero_documento = request.form.get('numeroDocumento')
        tipo_documento = request.form.get('tipoDocumento')
        
        db = SessionLocal()  # Iniciamos la sesión de la base de datos
        try:
            # Buscar el cliente usando la misma sesión
            cliente = Clientes.buscar_cliente_por_documento(db, tipo_documento, numero_documento)

            if cliente and not cliente.is_deleted:
                # Usar el método del modelo para eliminar al cliente
                Clientes.eliminar_cliente(db, cliente)
                flash('Cliente eliminado correctamente.', 'success')
            else:
                flash('Cliente no encontrado o ya eliminado.', 'danger')
        except Exception as e:
            db.rollback()  # Rollback si hay error
            flash(f'Error al eliminar el cliente: {str(e)}', 'danger')
        finally:
            db.close()  # Cerrar la sesión después de la operación

        # Redirigir a la página donde se ven todos los clientes
        return redirect(url_for('ver_clientes'))
    
    #-----------

    #Ruta para buscar cliente por numero de documento
    @app.route('/buscar_clientes_por_numero_documento')
    def buscar_clientes_por_numero_documento():
        query = request.args.get('q', '')
        
        # Llamada al método en el modelo para buscar clientes
        clientes_data = Clientes.buscar_por_numero_documento(query)

        # Si hubo un error, devolvemos un error en formato JSON
        if 'error' in clientes_data:
            return jsonify(clientes_data), 500

        # Devolvemos los datos de los clientes
        return jsonify(clientes_data)
    
    #------------------

    #Ruta para validar los datos de un cliente
    @app.route('/validar_cliente', methods=['POST'])
    def validar_cliente():
        data = request.get_json()
        
        # Llamada al método de validación en el modelo
        errores = Clientes.validar_datos(
            numero_documento=data.get('numeroDocumento'),
            email=data.get('emailCliente')
        )

        # Si hay errores, retornar con código 400
        if errores:
            return jsonify({'status': 'error', 'errores': errores}), 400

        return jsonify({'status': 'success'})
    
    #---------------------


    
