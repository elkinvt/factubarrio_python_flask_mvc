from src.app import app 
from flask_controller import FlaskController
from flask import request, redirect, url_for, flash, render_template, jsonify
from src.models import SessionLocal
from src.models.productos import Productos  # Importa el modelo de Productos
from src.models.categorias import Categoria #Importar el modelo de categorias
from src.models.unidad_medida import UnidadMedida #Importar el modelo unidad medida

class Productos_Controller(FlaskController):

    # Ruta para ver productos
    @app.route('/productos_ver', methods=['GET'])
    def productos_ver():
        try:
            # Usar el método que obtienes con el JOIN de productos, categorías y unidades de medida
            productos = Productos.obtener_productos()

            # Formatear el precio con separadores de miles y dos decimales
            for producto, categoria, unidad_medida in productos:
                if producto.precio_unitario is not None:
                    producto.precio_unitario_formateado = "{:,.2f}".format(producto.precio_unitario)
                else:
                    producto.precio_unitario_formateado = "N/A"

        except Exception as e:
            flash(f'Error al obtener productos: {str(e)}', 'danger')
            productos = []  # En caso de error, asignamos una lista vacía para evitar fallos en la vista

        return render_template('form_ver_producto.html', titulo_pagina="Ver Productos", productos=productos)

    
    #-------------------

    # Ruta para crear un producto (GET para mostrar formulario, POST para recibir datos)
    @app.route('/productos_crear', methods=['GET', 'POST'])
    def productos_crear():
        if request.method == 'POST':
            # Recibe los datos enviados desde el formulario
            codigo = request.form['codigoProducto']
            nombre = request.form['nombreProducto'].capitalize()
            descripcion = request.form['descripcionProducto'].capitalize()
            categoria = request.form['categoriaProducto']

            # Convertimos el precio a flotante y lo redondeamos a 2 decimales
            try:
                precio = float(request.form['precioProducto'].replace(',', ''))
                precio = round(precio, 2)  # Redondeamos a dos decimales
            except ValueError:
                flash('Precio no válido', 'danger')
                return redirect(url_for('productos_crear'))

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
                precio_unitario=precio  # Guardamos el precio redondeado
            )

            try:
                Productos.agregar_producto(nuevo_producto)
                flash('Producto creado con éxito', 'success')
            except Exception as e:
                flash(f'Error al crear producto: {str(e)}', 'danger')

            return redirect(url_for('ver_productos'))
        
        try:
            # Usar los métodos del modelo para obtener las categorías y unidades de medida
            categorias = Categoria.obtener_todas()  # Método en el modelo Categoria
            unidades_padre, subunidades = UnidadMedida.obtener_todas_con_subunidades()  # Método en el modelo UnidadMedida

        except Exception as e:
            flash(f'Error al cargar datos: {str(e)}', 'danger')

        return render_template('form_crear_producto.html', categorias=categorias, unidades_padre=unidades_padre, subunidades=subunidades, titulo_pagina="Crear Producto")

    #------------------
    
    # Ruta para buscar o seleccionar el producto
    @app.route('/productos_editar', methods=['GET'])
    def productos_editar():
        
        # Obtener el término de búsqueda (si existe)
        termino = request.args.get('termino', '').lower()
        producto_id = request.args.get('producto_id')  # ID del producto seleccionado

        try:
            # Fase 1: Si no hay término ni producto_id, mostramos solo el formulario de búsqueda
            if not termino and not producto_id:
                return render_template('form_editar_producto.html', productos=[], producto=None, 
                                    titulo_pagina="Buscar Producto")

            # Fase 2: Si hay término, buscar los productos correspondientes
            if termino:
                productos = Productos.buscar_por_codigo_o_nombre(termino)

                # Si no se encuentran productos, mostramos un mensaje flash
                if not productos:
                    flash('No se encontraron productos con ese nombre o código', 'warning')

                # Mostrar resultados de búsqueda, pero sin formulario de edición aún
                return render_template('form_editar_producto.html', productos=productos, producto=None, 
                                    titulo_pagina="Seleccionar Producto")

            # Fase 3: Si se seleccionó un producto por ID, cargar los detalles del producto
            if producto_id:
                producto = Productos.obtener_por_id(producto_id)
                categorias = Categoria.obtener_todas()
                unidades_padre, subunidades = UnidadMedida.obtener_todas_con_subunidades()

                # Mostrar el formulario de edición con los detalles del producto seleccionado
                return render_template('form_editar_producto.html', productos=[], producto=producto, 
                                    categorias=categorias, unidades_padre=unidades_padre, subunidades=subunidades, 
                                    titulo_pagina="Editar Producto")

        except Exception as e:
            flash(f'Error al procesar la solicitud: {str(e)}', 'danger')
            return render_template('form_editar_producto.html', productos=[], producto=None, 
                                titulo_pagina="Error")

    #--------------------

    # Ruta para mostrar el formulario con los datos del producto a editar
    @app.route('/productos_editar/<int:id>', methods=['GET'])
    def mostrar_formulario_editar_producto(id):
        try:
            # Usar el método del modelo para obtener el producto por ID
            producto = Productos.obtener_por_id(id)
            categorias = Categoria.obtener_todas()   # Obtener todas las categorías
            unidades_padre, subunidades = UnidadMedida.obtener_todas_con_subunidades()  # Obtener todas las unidades de medida

            if producto:
                # Pasar los datos del producto a la plantilla
                return render_template('form_editar_producto.html', producto=producto, categorias=categorias, unidades_padre=unidades_padre, 
            subunidades=subunidades, titulo_pagina="Editar Producto ")
            else:
                flash('Producto no encontrado.', 'danger')
                return redirect(url_for('buscar_producto'))
            
        except Exception as e:
            flash(f'Error al cargar datos: {str(e)}', 'danger')
            return redirect(url_for('buscar_producto'))
        
    #--------------------------

    # Ruta para actualizar el producto (POST)
    @app.route('/productos_actualizar/<int:id>', methods=['POST'])
    def actualizar_producto(id):
        try:
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
            producto = Productos.actualizar_producto(id, datos_actualizados)
            if producto:
                flash('Producto actualizado correctamente.', 'success')
            else:
                flash('Producto no encontrado.', 'danger')

        except Exception as e:
            flash(f'Error al actualizar producto: {str(e)}', 'danger')

        return redirect(url_for('ver_productos'))

    
    #---------------

    # Ruta para activar o desactivar un Producto
    @app.route('/productos_toggle_estado', methods=['POST'])
    def toggle_estado_producto():
        idproducto = request.form['idproducto']  # Recibimos el id del producto

        try:
            # Llamamos al método del modelo para cambiar el estado del producto
            nuevo_estado = Productos.toggle_estado(idproducto)
            if nuevo_estado is not None:
                
                estado = 'activado' if nuevo_estado else 'desactivado'
                flash(f'Producto {estado} con éxito.', 'success')
            else:
                flash('Producto no encontrado.', 'danger')
        except Exception as e:
            flash(f'Error al cambiar el estado del producto: {str(e)}', 'danger')
        
        return redirect(url_for('ver_productos'))
    
    #------------------
    

    # Ruta para eliminar un producto (eliminación lógica)
    @app.route('/productos_eliminar', methods=['POST'])
    def eliminar_producto():
        id_producto = request.form['idProducto']  # Obtener el ID del producto desde el formulario

        try:
            # Usar el método en el modelo para obtener el producto por ID
            eliminado = Productos.eliminar_producto(id_producto)
            
            if eliminado:
                
                flash('Producto eliminado con éxito.', 'success')
            else:
                flash('Producto no encontrado.', 'danger')

        except Exception as e:
            flash(f'Error al eliminar el producto: {str(e)}', 'danger')


        return redirect(url_for('ver_productos'))
    
    #------------------
    
    # Ruta para agregar los productos a la factura
    @app.route('/buscar_productos')
    def buscar_productos():
        query = request.args.get('q', '').lower()
        
        try:
            
            productos_data = Productos.buscar_productos_por_nombre(query)
            return jsonify(productos_data)
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    #-------------------

    # Ruta para verificar producto y stock
    @app.route('/verificar_producto')
    def verificar_producto():
        codigo = request.args.get('codigo')
        cantidad = int(request.args.get('cantidad'))

        try:
            # Llamar al método del modelo para verificar el producto y su stock
            resultado = Productos.verificar_stock_producto(codigo, cantidad)

            # Verificar si hay algún error en el resultado
            if 'error' in resultado:
                return jsonify(resultado), 200
            else:
                return jsonify(resultado)
        except Exception as e:
            return jsonify({'error': str(e)}), 500
 
    #--------------