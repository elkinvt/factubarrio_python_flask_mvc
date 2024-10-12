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

            '''return redirect(url_for('crear_vendedor'))'''

        return render_template('form_crear_vendedor.html', titulo_pagina="Crear vendedor")


    # Ruta para mostrar el formulario de edición (GET)
    @app.route('/vendedores_editar', methods=['GET'])
    def mostrar_formulario_editar_vendedor():
        tipo_documento = request.args.get('tipoDocumento')
        numero_documento = request.args.get('numeroDocumento')

        # Verificar si se ingresan ambos campos
        if not tipo_documento or not numero_documento:
            return render_template('form_editar_vendedor.html',vendedor=None, titulo_pagina="Editar Vendedor")

        db = SessionLocal()
        vendedor = db.query(Vendedores).filter_by(
            tipo_documento=tipo_documento,
            numero_documento=numero_documento,
            is_deleted=False
        ).first()
        db.close()

        if vendedor:
            return render_template('form_editar_vendedor.html', vendedor=vendedor, titulo_pagina="Editar Vendedor")
        else:
            flash("Vendedor no encontrado", 'danger')  # Usa flash para el error
            return render_template('form_editar_vendedor.html', mensaje="Vendedor no encontrado", vendedor=None, titulo_pagina="Editar Vendedor")

    # Buscar vendedor
    @app.route('/vendedores_buscar', methods=['GET'])
    def buscar_vendedor():
        tipo_documento = request.args.get('tipoDocumento')
        numero_documento = request.args.get('numeroDocumento')

        # Verificar si se ingresan ambos campos
        if not tipo_documento or not numero_documento:
            flash("Faltan datos de búsqueda", 'danger')
            return redirect(url_for('ver_vendedores'))

        db = SessionLocal()
        vendedor = db.query(Vendedores).filter_by(
            tipo_documento=tipo_documento,
            numero_documento=numero_documento,
            is_deleted=False  # Aseguramos que el vendedor no esté marcado como eliminado
        ).first()
        db.close()

        if vendedor:
            # Renderizar la plantilla de edición con los datos del vendedor
            return render_template('form_editar_vendedor.html', vendedor=vendedor, titulo_pagina="Editar Vendedor")
        else:
            flash("Vendedor no encontrado", 'danger')
            return redirect(url_for('ver_vendedores'))


    # Actualizar vendedor
    @app.route('/vendedores_actualizar', methods=['POST'])
    def actualizar_vendedor():
        db = SessionLocal()
        vendedor_id = request.form['vendedorId']  # ID del vendedor
        tipo_documento = request.form['tipoDocumento']
        numero_documento = request.form['numeroDocumento']
        nombre = request.form['nombreVendedor']
        telefono = request.form['telefonoVendedor']
        direccion = request.form['direccionVendedor']
        email = request.form['emailVendedor']

        # Buscar al vendedor por su idvendedores
        vendedor = db.query(Vendedores).filter_by(idvendedores=vendedor_id).first()

        if vendedor:
            # Actualizar los campos del vendedor
            vendedor.tipo_documento = tipo_documento
            vendedor.numero_documento = numero_documento
            vendedor.nombres_vendedor = nombre
            vendedor.telefono = telefono
            vendedor.direccion = direccion
            vendedor.email = email

            try:
                db.commit()  # Guardar los cambios en la base de datos
                flash('Cambios guardados correctamente', 'success')
            except Exception as e:
                db.rollback()  # Deshacer los cambios si hay un error
                flash(f'Error al guardar los cambios: {str(e)}', 'danger')
        else:
            flash('Vendedor no encontrado', 'danger')

        db.close()
        # Redirigir a la página de lista de vendedores
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
