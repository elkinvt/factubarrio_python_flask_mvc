from flask import request, redirect, url_for, flash, render_template, jsonify
from models import SessionLocal
from models.vendedores import Vendedores

def registrar_rutas(app):
    # Crear vendedor
    @app.route('/vendedores_crear', methods=['GET', 'POST'])
    def crear_vendedor():
        if request.method == 'POST':
            db = SessionLocal()
            tipo_documento = request.form['tipoDocumento']
            numero_documento = request.form['numeroDocumento']
            nombre = request.form['nombreVendedor']
            apellido = request.form['apellidoVendedor']
            telefono = request.form['telefonoVendedor']
            direccion = request.form['direccionVendedor']
            email = request.form['emailVendedor']

            nuevo_vendedor = Vendedores(
                tipo_documento=tipo_documento,
                numero_documento=numero_documento,
                nombre=nombre,
                apellido=apellido,
                telefono=telefono,
                direccion=direccion,
                email=email
            )

            try:
                db.add(nuevo_vendedor)
                db.commit()
                flash('Vendedor creado con éxito', 'success')
            except Exception as e:
                db.rollback()
                flash(f'Error al crear vendedor: {str(e)}', 'danger')
            finally:
                db.close()

            return redirect(url_for('crear_vendedor'))

        return render_template('form_crear_vendedor.html', titulo_pagina="Crear vendedor")

    # Ver vendedores
    @app.route('/vendedores_ver', methods=['GET'])
    def ver_vendedores():
        db = SessionLocal()
        vendedores = db.query(Vendedores).filter_by(is_deleted=False).all()
        db.close()
        return render_template('form_ver_vendedor.html', titulo_pagina="Ver Vendedores", vendedores=vendedores)

    # Buscar vendedor
    @app.route('/vendedores_buscar', methods=['GET'])
    def buscar_vendedor():
        tipo_documento = request.args.get('tipoDocumento').strip().upper()
        numero_documento = request.args.get('numeroDocumento').strip()

        db = SessionLocal()
        vendedor = db.query(Vendedores).filter(
            Vendedores.tipo_documento == tipo_documento,
            Vendedores.numero_documento == numero_documento
        ).first()
        db.close()

        if vendedor:
            return jsonify({
                'id': vendedor.id,
                'tipo_documento': vendedor.tipo_documento,
                'numero_documento': vendedor.numero_documento,
                'nombre': vendedor.nombre,
                'apellido': vendedor.apellido,
                'telefono': vendedor.telefono,
                'direccion': vendedor.direccion,
                'email': vendedor.email
            })
        else:
            return jsonify({'error': 'Vendedor no encontrado'}), 404

    # Actualizar vendedor
    @app.route('/vendedores_actualizar', methods=['POST'])
    def actualizar_vendedor():
        db = SessionLocal()
        vendedor_id = request.form['vendedorId']
        tipo_documento = request.form['tipoDocumento']
        numero_documento = request.form['numeroDocumento']
        nombre = request.form['nombreVendedor']
        apellido = request.form['apellidoVendedor']
        telefono = request.form['telefonoVendedor']
        direccion = request.form['direccionVendedor']
        email = request.form['emailVendedor']

        vendedor = db.query(Vendedores).filter_by(id=vendedor_id).first()

        if vendedor:
            vendedor.tipo_documento = tipo_documento
            vendedor.numero_documento = numero_documento
            vendedor.nombre = nombre
            vendedor.apellido = apellido
            vendedor.telefono = telefono
            vendedor.direccion = direccion
            vendedor.email = email

            try:
                db.commit()
                flash('Cambios guardados correctamente', 'success')
            except Exception as e:
                db.rollback()
                flash(f'Error al guardar los cambios: {str(e)}', 'danger')
        else:
            flash('Vendedor no encontrado', 'danger')

        db.close()
        return redirect(url_for('ver_vendedores'))

    # Eliminar vendedor
    @app.route('/vendedores_eliminar', methods=['POST'])
    def eliminar_vendedor():
        data = request.get_json()
        numero_documento = data.get('numeroDocumento')
        tipo_documento = data.get('tipoDocumento')

        db = SessionLocal()

        try:
            vendedor = db.query(Vendedores).filter_by(numero_documento=numero_documento, tipo_documento=tipo_documento).first()

            if vendedor and not vendedor.is_deleted:
                vendedor.is_deleted = True

                try:
                    db.commit()
                    return jsonify({'success': True, 'message': 'Vendedor eliminado correctamente.'})
                except Exception as e:
                    db.rollback()
                    return jsonify({'success': False, 'message': f'Error al eliminar el vendedor: {str(e)}'})
            else:
                return jsonify({'success': False, 'message': 'Vendedor no encontrado o ya eliminado.'}), 404
        finally:
            db.close()
