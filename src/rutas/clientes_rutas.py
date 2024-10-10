from flask import request, redirect, url_for, flash, render_template, jsonify
from models import SessionLocal
from models.clientes import Clientes



# Función para registrar las rutas en la aplicación Flask
def registrar_rutas(app):
    
    # Ruta para ver todos los clientes
    @app.route('/clientes_ver', methods=['GET'])
    def ver_clientes():
        # Obtener los clientes desde el modelo Clientes
        clientes = Clientes.obtener_clientes()
        return render_template('form_ver_cliente.html', titulo_pagina="Ver Clientes", clientes=clientes)
    
    

    
    #Ruta para crear el cliente
    @app.route('/clientes_crear', methods=['GET', 'POST'])
    def crear_cliente():
        if request.method == 'POST':
            # Procesar el formulario enviado
            db = SessionLocal()

            # Obtener los datos del formulario
            tipo_documento = request.form['tipoDocumento']
            numero_documento = request.form['numeroDocumento']
            nombres_cliente = request.form['nombreCliente']
            telefono = request.form['telefonoCliente']
            direccion = request.form['direccionCliente']
            email = request.form['emailCliente']

            # Crear el cliente con los datos recibidos
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
                return redirect(url_for('crear_cliente'))  # Redirigir al formulario después de crear el cliente
            except Exception as e:
                db.rollback()  # Deshacer cambios si ocurre un error
                flash(f'Error al crear cliente: {str(e)}', 'danger')
            finally:
                db.close()

        # Si es GET, mostrar el formulario
        return render_template('form_crear_cliente.html', titulo_pagina="Crear Cliente")
    
    
      
    

    # Ruta para mostrar el formulario de edición (GET)
    @app.route('/clientes_editar', methods=['GET'])
    def mostrar_formulario_editar_cliente():
        tipo_documento = request.args.get('tipoDocumento')
        numero_documento = request.args.get('numeroDocumento')

        # Verificar si se ingresan ambos campos
        if not tipo_documento or not numero_documento:
            flash('Por favor, ingrese ambos campos: Tipo de Documento y Número de Documento.', 'warning')
            return render_template('form_editar_cliente.html', cliente=None, titulo_pagina="Editar Cliente")

        cliente = Clientes.buscar_cliente_por_documento(tipo_documento, numero_documento)

        if cliente:
            print(f"Cliente encontrado: {cliente.nombres_cliente}, is_deleted: {cliente.is_deleted}")  # Depuración
            if cliente.is_deleted:
                flash('Este cliente ha sido eliminado y no puede ser editado.', 'danger')
                return render_template('form_editar_cliente.html', cliente=None, titulo_pagina="Cliente Eliminado")
            else:
                return render_template('form_editar_cliente.html', cliente=cliente, titulo_pagina="Editar Cliente")
        else:
            flash('Cliente no encontrado. Verifique los datos ingresados.', 'danger')
            return render_template('form_editar_cliente.html', cliente=None, titulo_pagina="Editar Cliente")




    # Ruta para actualizar un cliente (POST)
    @app.route('/clientes_actualizar', methods=['POST'])
    def actualizar_cliente():
        cliente_id = request.form['clienteId']
        tipo_documento = request.form['tipoDocumento']
        numero_documento = request.form['numeroDocumento']
        nombres_cliente = request.form['nombreCliente']
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

            try:
                Clientes.actualizar_cliente(db, cliente, datos_actualizados)
                flash('Cambios guardados correctamente', 'success')
                return redirect(url_for('mostrar_formulario_editar_cliente'))
            except Exception as e:
                flash(f'Error al guardar los cambios: {str(e)}', 'danger')
        else:
            flash('Cliente no encontrado', 'danger')

        db.close()
        return redirect(url_for('mostrar_formulario_editar_cliente', tipoDocumento=tipo_documento, numeroDocumento=numero_documento))
    
    
    
    
    
    
    
    
    
    
    
    
    #ruta para actualizar el estado de un cliente
    @app.route('/clientes_toggle_estado', methods=['POST'])
    def toggle_estado_cliente():
        db = SessionLocal()
        numero_documento = request.form['numeroDocumento']
        tipo_documento = request.form['tipoDocumento']

        try:
            # Buscar el cliente usando el tipo y número de documento
            cliente = db.query(Clientes).filter_by(numero_documento=numero_documento, tipo_documento=tipo_documento).first()
            if cliente:
                # Cambiar el estado (activo/inactivo)
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

        # Redirigir a la página donde corresponda
        return redirect(url_for('mostrar_formulario_editar_cliente', cliente_id=cliente.idclientes))

    # Ruta para eliminar cliente (lógica)
    @app.route('/clientes_eliminar', methods=['POST'])
    def eliminar_cliente():
        numero_documento = request.form.get('numeroDocumento')
        tipo_documento = request.form.get('tipoDocumento')
        
        db = SessionLocal()
        cliente = db.query(Clientes).filter_by(numero_documento=numero_documento, tipo_documento=tipo_documento).first()

        if cliente and not cliente.is_deleted:
            cliente.is_deleted = True

            try:
                db.commit()
                flash('Cliente eliminado correctamente.', 'success')
            except Exception as e:
                db.rollback()
                flash(f'Error al eliminar el cliente: {str(e)}', 'danger')
        else:
            flash('Cliente no encontrado o ya eliminado.', 'danger')
        
        db.close()
        # Redirigir a la página donde se ven todos los clientes
        return redirect(url_for('ver_clientes'))

