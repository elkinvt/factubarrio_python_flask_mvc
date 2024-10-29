from src.app import app 
from flask_controller import FlaskController
from flask import request, redirect, url_for, flash, render_template, jsonify
from src.models import db_session_manager
from src.models.vendedores import Vendedores

class Vendedores_Controller(FlaskController):
    # Ruta para ver todos los vendedores
    @app.route('/vendedores_ver', methods=['GET'])
    def ver_vendedores():
        vendedores = Vendedores.obtener_vendedores()
        return render_template('form_ver_vendedor.html', titulo_pagina="Ver Vendedores", vendedores=vendedores)

    #--------------
    
    # Crear vendedor
    @app.route('/vendedores_crear', methods=['GET', 'POST'])
    def crear_vendedor():
        if request.method == 'POST':
            tipo_documento = request.form['tipoDocumento']
            numero_documento = request.form['numeroDocumento']
            nombre_completo = request.form['nombreVendedor'].title()  # Usamos un solo campo para el nombre completo
            telefono = request.form['telefonoVendedor']
            direccion = request.form['direccionVendedor']
            email = request.form['emailVendedor']

             # Validar si hay datos duplicados antes de crear el cliente
            errores = Vendedores.validar_datos(numero_documento=numero_documento, email=email)

            if errores:
                # Si hay errores de duplicados, mostrar un mensaje y no guardar
                for campo, mensaje in errores.items():
                    flash(f"{mensaje}", 'danger')
                return redirect(url_for('crear_vendedor'))  # Redirige de vuelta al formulario

            # Creando el objeto del nuevo vendedor con el modelo que ya tienes en la base de datos
            nuevo_vendedor = Vendedores(
                tipo_documento=tipo_documento,
                numero_documento=numero_documento,
                nombres_vendedor=nombre_completo,  # Insertamos el nombre completo
                telefono=telefono,
                direccion=direccion,
                email=email
            )

            try:
                Vendedores.agregar_vendedor(nuevo_vendedor)
                flash('Vendedor creado con éxito', 'success')
                return redirect(url_for('ver_vendedores')) 
            except Exception as e:
                flash(f'Error al crear vendedor: {str(e)}', 'danger')
        

        # Si es GET, mostrar el formulario
        return render_template('form_crear_vendedor.html', titulo_pagina="Crear vendedor")
    
    #------------

   
    # Ruta para mostrar el formulario de edición (GET)
    @app.route('/vendedores_editar', methods=['GET'])
    def mostrar_formulario_editar_vendedor():
        tipo_documento = request.args.get('tipoDocumento')
        numero_documento = request.args.get('numeroDocumento')

        # Verificar si se ingresan ambos campos
        if not tipo_documento or not numero_documento:
            flash('Por favor, ingrese ambos campos: Tipo de Documento y Número de Documento.', 'warning')
            return render_template('form_editar_vendedor.html', vendedor=None, titulo_pagina="Editar Vendedor")

        try:
            # Llamar al método del modelo para buscar el vendedor sin manejar la sesión
            vendedor = Vendedores.buscar_vendedor_por_documento(tipo_documento, numero_documento)
            
            if vendedor:
                if vendedor.is_deleted:
                    flash('Este vendedor ha sido eliminado y no puede ser editado.', 'danger')
                    return render_template('form_editar_vendedor.html', vendedor=None, titulo_pagina="Vendedor Eliminado")
                return render_template('form_editar_vendedor.html', vendedor=vendedor, titulo_pagina="Editar Vendedor")
            else:
                flash('Vendedor no encontrado. Verifique los datos ingresados.', 'danger')
                return render_template('form_editar_vendedor.html', vendedor=None, titulo_pagina="Editar Vendedor")
        except Exception as e:
            flash(f'Error al buscar el vendedor: {str(e)}', 'danger')
            return render_template('form_editar_vendedor.html', vendedor=None, titulo_pagina="Error al Editar Vendedor")

    #------------

    # Actualizar vendedor
    @app.route('/vendedores_actualizar', methods=['POST'])
    def actualizar_vendedor():
        vendedor_id = request.form['vendedorId']
        tipo_documento = request.form['tipoDocumento']
        numero_documento = request.form['numeroDocumento']
        nombre = request.form['nombreVendedor'].title()
        telefono = request.form['telefonoVendedor']
        direccion = request.form['direccionVendedor']
        email = request.form['emailVendedor']

        # Diccionario de datos actualizados
        datos_actualizados = {
            'tipo_documento': tipo_documento,
            'numero_documento': numero_documento,
            'nombres_vendedor': nombre,
            'telefono': telefono,
            'direccion': direccion,
            'email': email
        }

        try:
            Vendedores.actualizar_vendedor(vendedor_id, datos_actualizados)
            flash('Cambios guardados correctamente.', 'success')
        except ValueError:
            flash('Vendedor no encontrado.', 'danger')
        except Exception as e:
            flash(f'Error al guardar los cambios: {str(e)}', 'danger')

        return redirect(url_for('ver_vendedores'))
        
    #------------------
    
   
    # Ruta para eliminar vendedor (lógica)
    @app.route('/vendedores_eliminar', methods=['POST'])
    def eliminar_vendedor():
        numero_documento = request.form.get('numeroDocumento')
        tipo_documento = request.form.get('tipoDocumento')
        
        try:
            # Buscar el cliente usando el método del modelo (sin necesidad de manejar la sesión)
            vendedor = Vendedores.buscar_vendedor_por_documento(tipo_documento, numero_documento)

            if vendedor and not vendedor.is_deleted:
                # Llamamos al método del modelo para eliminar al vendedor
                Vendedores.eliminar_vendedor(vendedor)
                flash('Vendedor eliminado correctamente.', 'success')
            else:
                flash('Vendedor no encontrado o ya eliminado.', 'danger')
        except Exception as e:
            flash(f'Error al eliminar el vendedor: {str(e)}', 'danger')

        # Redirigir a la página donde se ven todos los vendedores
        return redirect(url_for('ver_vendedores'))

    
    #-----------

    #Ruta para validar los datos de un cliente
    @app.route('/validar_vendedor', methods=['POST'])
    def validar_vendedor():
        data = request.get_json()
        
        # Llamada al método de validación en el modelo Vendedores
        errores = Vendedores.validar_datos(
            numero_documento=data.get('numeroDocumento'),
            email=data.get('emailVendedor')
        )

        # Si hay errores, retornar con código 400
        if errores:
            return jsonify({'status': 'error', 'errores': errores}), 400

        return jsonify({'status': 'success'})

    
    #---------------------
