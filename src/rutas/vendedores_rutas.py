from flask import request, redirect, url_for, flash, render_template
from models import SessionLocal
from models.vendedores import Vendedores

def registrar_rutas(app):
    
    # Ruta para ver todos los vendedores
    @app.route('/vendedores_ver', methods=['GET'])
    def ver_vendedores():
        # Obtener los clientes desde el modelo Clientes
        vendedores = Vendedores.obtener_vendedores()
        return render_template('form_ver_vendedor.html', titulo_pagina="Ver  Vendedores", vendedores=vendedores)
    
    #--------------
    
    # Crear vendedor
    @app.route('/vendedores_crear', methods=['GET', 'POST'])
    def crear_vendedor():
        if request.method == 'POST':
            db = SessionLocal()
            tipo_documento = request.form['tipoDocumento']
            numero_documento = request.form['numeroDocumento']
            nombre_completo = request.form['nombreVendedor']  # Usamos un solo campo para el nombre completo
            telefono = request.form['telefonoVendedor']
            direccion = request.form['direccionVendedor']
            email = request.form['emailVendedor']

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
                Vendedores.agregar_vendedor(db,nuevo_vendedor)
                flash('Vendedor creado con éxito', 'success')
                return redirect(url_for('crear_vendedor')) 
            except Exception as e:
                db.rollback()
                flash(f'Error al crear vendedor: {str(e)}', 'danger')
            finally:
                db.close()

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

        db = SessionLocal()

        try:
            # Usar la sesión en la función de búsqueda
            vendedor = Vendedores.buscar_vendedor_por_documento(db, tipo_documento, numero_documento)

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
        finally:
            db.close()  # Cerramos la sesión aquí después de obtener el vendedor

    # Actualizar vendedor
    @app.route('/vendedores_actualizar', methods=['POST'])
    def actualizar_vendedor():
        vendedor_id = request.form['vendedorId']
        tipo_documento = request.form['tipoDocumento']
        numero_documento = request.form['numeroDocumento']
        nombre = request.form['nombreVendedor']
        telefono = request.form['telefonoVendedor']
        direccion = request.form['direccionVendedor']
        email = request.form['emailVendedor']

        db = SessionLocal()  # Iniciar nueva sesión

        try:
            # Rebuscar al vendedor por su idvendedores para asegurarse de que está asociado a esta sesión
            vendedor = Vendedores.buscar_vendedor_por_id(vendedor_id)

            if vendedor:
                # Diccionario de datos actualizados
                datos_actualizados = {
                    'tipo_documento': tipo_documento,
                    'numero_documento': numero_documento,
                    'nombres_vendedor': nombre,
                    'telefono': telefono,
                    'direccion': direccion,
                    'email': email
                }

                # Verificar si el vendedor está en la sesión actual, si no lo está, reasociarlo
                if not db.object_session(vendedor):
                    db.add(vendedor)
                
                # Actualizar el vendedor utilizando el método en el modelo
                Vendedores.actualizar_vendedor(db, vendedor, datos_actualizados)
                flash('Cambios guardados correctamente.', 'success')
            else:
                flash('Vendedor no encontrado.', 'danger')

        except Exception as e:
            db.rollback()  # Deshacer los cambios si hay un error
            flash(f'Error al guardar los cambios: {str(e)}', 'danger')
        finally:
            db.close()  # Asegurar que la sesión se cierra correctamente

        return redirect(url_for('ver_vendedores'))


    
    
    
    
    
    
    
    
    
    
    
    
    

    # Eliminar vendedor
    @app.route('/vendedores_eliminar', methods=['POST'])
    def eliminar_vendedor():
        # Obtener los datos del formulario
        tipo_documento = request.form.get('tipoDocumento')
        numero_documento = request.form.get('numeroDocumento')

        db = SessionLocal()

        try:
            # Buscar el vendedor por tipo de documento y número de documento
            vendedor = db.query(Vendedores).filter_by(
                tipo_documento=tipo_documento,
                numero_documento=numero_documento
            ).first()

            if vendedor and not vendedor.is_deleted:
                # Marcar al vendedor como eliminado (eliminación lógica)
                vendedor.is_deleted = True

                try:
                    db.commit()
                    flash('Vendedor eliminado correctamente', 'success')
                except Exception as e:
                    db.rollback()
                    flash(f'Error al eliminar el vendedor: {str(e)}', 'danger')
            else:
                flash('Vendedor no encontrado o ya estaba eliminado.', 'danger')

        finally:
            db.close()

        # Redirigir a la lista de vendedores después de eliminar
        return redirect(url_for('ver_vendedores'))
