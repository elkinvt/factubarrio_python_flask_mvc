# Importa las dependencias necesarias
from flask import request, redirect, url_for, flash, render_template, jsonify
from models import SessionLocal
from models.productos import Productos  # Importa el modelo de Productos

# Función para registrar las rutas de productos en la aplicación Flask
def registrar_rutas(app):

   # Ruta para crear un producto (GET para mostrar formulario, POST para recibir datos)
    @app.route('/productos_crear', methods=['GET', 'POST'])
    def crear_producto():
        db = SessionLocal()

        if request.method == 'POST':
            # Recibe los datos enviados desde el formulario
            codigo = request.form['codigoProducto']
            nombre = request.form['nombreProducto']
            descripcion = request.form['descripcionProducto']
            categoria = request.form['categoriaProducto']
            precio = request.form['precioProducto']
            unidad_medida = request.form['unidadMedidaProducto']
            presentacion = request.form['presentacionProducto']
            cantidad_stock = request.form['cantidadStockProducto']

            # Crea una nueva instancia de Productos
            nuevo_producto = Productos(
                codigo=codigo,
                nombre=nombre,
                descripcion=descripcion,
                categoria_idcategoria=categoria,
                unidad_medida_idunidad_medida=unidad_medida,
                presentacion=presentacion,
                cantidad_stock=cantidad_stock,
                precio_unitario=precio
            )

            try:
                db.add(nuevo_producto)
                db.commit()
                flash('Producto creado con éxito', 'success')
            except Exception as e:
                db.rollback()
                flash(f'Error al crear producto: {str(e)}', 'danger')
            finally:
                db.close()

            return redirect(url_for('crear_producto'))

        # Cargar las categorías y unidades de medida desde la base de datos
        categorias = db.query(Categoria).all()  # Obtener todas las categorías
        unidades_padre = db.query(UnidadMedida).filter(UnidadMedida.unidad_padre_id == None).all()  # Obtener unidades padre
        unidades_hijas = db.query(UnidadMedida).filter(UnidadMedida.unidad_padre_id != None).all()  # Obtener unidades hijas
        db.close()

        return render_template('form_crear_producto.html', categorias=categorias, unidades_padre=unidades_padre, unidades_hijas=unidades_hijas, titulo_pagina="Crear Producto")


    
    
    
    
    

    # Ruta para ver productos
    @app.route('/productos_ver', methods=['GET'])
    def ver_productos():
        db = SessionLocal()
        productos = db.query(Productos).filter_by(is_deleted=False).all()
        db.close()
        return render_template('form_ver_producto.html', titulo_pagina="Ver Productos", productos=productos)

    # Ruta para buscar un producto por su código (ejemplo)
    @app.route('/productos_buscar', methods=['GET'])
    def buscar_producto():
        codigo = request.args.get('codigoProducto')
        db = SessionLocal()
        producto = db.query(Productos).filter_by(codigo=codigo).first()
        db.close()

        if producto:
            return jsonify({
                'id': producto.id,
                'codigo': producto.codigo,
                'nombre': producto.nombre,
                'descripcion': producto.descripcion,
                'categoria': producto.categoria,
                'precio': producto.precio,
                'unidad_medida': producto.unidad_medida,
                'presentacion': producto.presentacion,
                'cantidad_stock': producto.cantidad_stock,
                'is_active': producto.is_active
            })
        else:
            return jsonify({'error': 'Producto no encontrado'}), 404

    # Ruta para actualizar un producto
    @app.route('/productos_actualizar', methods=['POST'])
    def actualizar_producto():
        db = SessionLocal()
        producto_id = request.form['productoId']
        # (Recibe y actualiza los datos similares a la ruta de creación)
        # ...
        db.close()
        return redirect(url_for('ver_productos'))
    
    
    # Ruta para activar o desactivar un Producto
    @app.route('/productos_toggle_estado', methods=['POST'])
    def toggle_estado_producto():
        db = SessionLocal()
        codigo = request.form['codigoProducto']

        try:
            producto = db.query(Productos).filter_by(codigo=codigo).first()
            if producto:
                producto.is_active = not producto.is_active
                db.commit()
                estado = 'activado' if producto.is_active else 'desactivado'
                flash(f'Producto {estado} con éxito.', 'success')
            else:
                flash('Producto no encontrado.', 'danger')
        except Exception as e:
            db.rollback()
            flash(f'Error al cambiar el estado del producto: {str(e)}', 'danger')
        finally:
            db.close()

        return redirect(url_for('ver_productos'))


    # Ruta para eliminar un producto (eliminación lógica)
    @app.route('/productos_eliminar', methods=['POST'])
    def eliminar_producto():
        db = SessionLocal()
        codigo = request.form['codigoProducto']
        producto = db.query(Productos).filter_by(codigo=codigo).first()
        
        if producto:
            producto.is_deleted = True
            try:
                db.commit()
                flash('Producto eliminado correctamente', 'success')
            except Exception as e:
                db.rollback()
                flash(f'Error al eliminar producto: {str(e)}', 'danger')
        else:
            flash('Producto no encontrado', 'danger')
        
        db.close()
        return redirect(url_for('ver_productos'))
