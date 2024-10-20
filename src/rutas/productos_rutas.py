# Importa las dependencias necesarias
from flask import request, redirect, url_for, flash, render_template, jsonify
from src.models import SessionLocal
from src.models.productos import Productos  # Importa el modelo de Productos
from src.models.categorias import Categoria
from src.models.unidad_medida import UnidadMedida




# Función para registrar las rutas de productos en la aplicación Flask
def registrar_rutas(app):

    # Ruta para crear un producto (GET para mostrar formulario, POST para recibir datos)
    @app.route('/productos_crear', methods=['GET', 'POST'])
    def crear_producto():
        db = SessionLocal()

        if request.method == 'POST':
            # Recibe los datos enviados desde el formulario
            codigo = request.form['codigoProducto']
            nombre = request.form['nombreProducto'].capitalize()
            descripcion = request.form['descripcionProducto'].capitalize()
            categoria = request.form['categoriaProducto']
            precio = float(request.form['precioProducto'])  # Convertimos a float
            unidad_medida = request.form['unidadMedidaProducto']
            presentacion = request.form['presentacionProducto']
            cantidad_stock = int(request.form['cantidadStockProducto'])  # Convertimos a int

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

            return redirect(url_for('ver_productos'))

        try:
            # Usar los métodos del modelo para obtener las categorías y unidades de medida
            categorias = Categoria.obtener_todas(db)  # Método en el modelo Categoria
            unidades_padre, subunidades = UnidadMedida.obtener_todas_con_subunidades(db)  # Método en el modelo UnidadMedida

        except Exception as e:
            flash(f'Error al cargar datos: {str(e)}', 'danger')
        finally:
            db.close()  # Cerrar sesión incluso en GET

        return render_template('form_crear_producto.html', categorias=categorias, unidades_padre=unidades_padre, subunidades=subunidades, titulo_pagina="Crear Producto")

    #------------------
    
    # Ruta para ver productos
    @app.route('/productos_ver', methods=['GET'])
    def ver_productos():
        db = SessionLocal()
        try:
            # Usar el método que obtienes con el JOIN de productos, categorías y unidades de medida
            productos = Productos.obtener_productos()
        except Exception as e:
            flash(f'Error al obtener productos: {str(e)}', 'danger')
            productos = []  # En caso de error, asignamos una lista vacía para evitar fallos en la vista
        finally:
            db.close()  # Aseguramos el cierre de la sesión

        return render_template('form_ver_producto.html', titulo_pagina="Ver Productos", productos=productos)
    
    #-------------------


    # Ruta para mostrar el formulario de edición de productos (GET)
    @app.route('/productos_editar', methods=['GET'])
    def mostrar_formulario_edicion_producto():
        # Renderiza el formulario vacío, con los campos del producto sin datos
        return render_template('form_editar_producto.html', producto=None, categorias=[], unidades_medida=[], titulo_pagina="Editar Producto")

    #--------------
    
    # Ruta para buscarr el producto por el nombre o codigo (GET)
    @app.route('/productos_buscar', methods=['GET'])
    def buscar_producto():
        termino = request.args.get('termino', '').lower()
        db = SessionLocal()

        try:
            productos = Productos.buscar_por_codigo_o_nombre(termino, db)
            categorias = Categoria.obtener_todas(db)  # Método en el modelo Categoria
            unidades_padre, subunidades = UnidadMedida.obtener_todas_con_subunidades(db)  # Método en el modelo UnidadMedida
            
            
            # Renderizar la misma plantilla con los productos y los datos adicionales
            return render_template('form_editar_producto.html', productos=productos, categorias=categorias, unidades_padre=unidades_padre, 
            subunidades=subunidades, titulo_pagina="Seleccionar producto")

        except Exception as e:
            flash(f'Error al buscar el producto: {str(e)}', 'danger')
            return render_template('form_editar_producto.html', productos=[], categorias=[], unidades_medida=[])
        
        finally:
            db.close()
    
    #-------------------

    # Ruta para mostrar el formulario con los datos del producto a editar
    @app.route('/productos_editar/<int:id>', methods=['GET'])
    def mostrar_formulario_editar_producto(id):
        db = SessionLocal()
        try:
            # Usar el método del modelo para obtener el producto por ID
            producto = Productos.obtener_por_id(id, db)
            categorias = Categoria.obtener_todas(db)   # Obtener todas las categorías
            unidades_padre, subunidades = UnidadMedida.obtener_todas_con_subunidades(db)  # Obtener todas las unidades de medida

            if producto:
                # Pasar los datos del producto a la plantilla
                return render_template('form_editar_producto.html', producto=producto, categorias=categorias, unidades_padre=unidades_padre, 
            subunidades=subunidades, titulo_pagina="Editar Producto ")
            else:
                flash('Producto no encontrado.', 'danger')
                return redirect(url_for('buscar_producto'))
        finally:
            db.close()

            
    #--------------------------

    # Ruta para actualizar el producto (POST)
    @app.route('/productos_actualizar/<int:id>', methods=['POST'])
    def actualizar_producto(id):
        db = SessionLocal()
        
        try:
            # Usamos el método del modelo para obtener el producto por ID
            producto = Productos.obtener_por_id(id, db)
            
            if producto:
                # Diccionario de datos actualizados
                datos_actualizados = {
                    'codigo': request.form['codigo'],
                    'nombre': request.form['nombre'].capitalize(),
                    'descripcion': request.form['descripcion'].capitalize(),
                    'categoria_idcategoria': request.form['categoria_id'],
                    'unidad_medida_idunidad_medida': request.form['unidadMedidaProducto'],
                    'presentacion': request.form['presentacion'],
                    'cantidad_stock': request.form['cantidad_stock'],
                    'precio_unitario': request.form['precio']
                }

                # Usamos el método del modelo para actualizar el producto
                Productos.actualizar_producto(producto, datos_actualizados, db)
                flash('Producto actualizado correctamente.', 'success')
            else:
                flash('Producto no encontrado.', 'danger')
        
        except Exception as e:
            db.rollback()
            flash(f'Error al actualizar producto: {str(e)}', 'danger')
        
        finally:
            db.close()
        
        return redirect(url_for('ver_productos'))

    
    #---------------

    # Ruta para activar o desactivar un Producto
    @app.route('/productos_toggle_estado', methods=['POST'])
    def toggle_estado_producto():
        db = SessionLocal()
        idproducto = request.form['idproducto']  # Recibimos el id del producto

        try:
            # Utilizamos el método obtener_por_id para buscar el producto
            producto = Productos.obtener_por_id(idproducto, db)
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
        id_producto = request.form['idProducto']  # Obtener el ID del producto desde el formulario

        try:
            # Usar el método en el modelo para obtener el producto por ID
            producto = Productos.obtener_por_id(id_producto, db)
            
            if producto:
                # Realizar eliminación lógica
                producto.is_deleted = True
                db.commit()
                flash('Producto eliminado con éxito.', 'success')
            else:
                flash('Producto no encontrado.', 'danger')

        except Exception as e:
            db.rollback()
            flash(f'Error al eliminar el producto: {str(e)}', 'danger')

        finally:
            db.close()

        return redirect(url_for('ver_productos'))
    
    #------------------
    
    # Ruta para agregar los productos a la factura
    @app.route('/buscar_productos')
    def buscar_productos():
        query = request.args.get('q', '').lower()
        db = SessionLocal()
        try:
            productos = db.query(Productos).filter(Productos.nombre.ilike(f'%{query}%')).filter(Productos.is_deleted == False).all()
            productos_data = [{'id': producto.idproductos, 'codigo': producto.codigo,  'nombre': producto.nombre,'descripcion': producto.descripcion, 'precio_unitario': float(producto.precio_unitario)} for producto in productos]
            return jsonify(productos_data)
        finally:
            db.close()


