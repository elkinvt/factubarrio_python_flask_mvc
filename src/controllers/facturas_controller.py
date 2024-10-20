from src.app import app 
from flask_controller import FlaskController
from flask import request, redirect, url_for, flash, render_template
from flask import render_template, request, redirect, url_for, flash, jsonify
from src.models.vendedores import Vendedores  # Importar la clase Vendedores
from src.models.productos import Productos  # Importar la clase Productos
from src.models.facturas import Factura  # Importar la clase Factura
from src.models.detalle_producto import DetalleProducto  # Importar DetalleProducto
from src.models import SessionLocal # Importar la sesión para interactuar con la base de datos
from datetime import datetime
import json


class Facturas_Controller(FlaskController):

    #Ruta para cargar la vista de facturas
    @app.route('/ver_factura')
    def ver_factura():
        return render_template('form_ver_factura.html', titulo_pagina = "Ver factura")
    
    #---------

    #Ruta para generar la factura
    @app.route('/generar_factura', methods=['GET', 'POST'])
    def factura_crear():
        db = SessionLocal()

        if request.method == 'POST':
            try:
                
                # Recibe los datos del formulario
                clientes_idclientes = request.form.get('clienteId')
                vendedores_idvendedores = request.form.get('vendedorFactura')
                productos = json.loads(request.form.get('productosFactura'))
                
                # Logs para verificar los datos recibidos
                print(f"Cliente ID: {clientes_idclientes}")
                print(f"Vendedor ID: {vendedores_idvendedores}")
                print(f"Productos: {productos}")

                # Calcular el total de la factura
                total_valor = sum([float(item['precio']) * int(item['cantidad']) for item in productos])
                print(f"Total Valor: {total_valor}")  # Log del total calculado

                impuesto = total_valor * 0.19  # Impuesto del 19%
                print(f"Impuesto: {impuesto}")  # Log del impuesto calculado

                descuento = float(request.form.get('descuentoFactura', 0))
                print(f"Descuento: {descuento}")  # Log del descuento recibido

                total_final = total_valor + impuesto - descuento

                # Recibir los valores de pago y calcular el cambio
                monto_pagado = float(request.form.get('monto_pagado'))
                print(f"Monto Pagado: {monto_pagado}")  # Log del monto pagado recibido
                
                if monto_pagado < total_final:
                    raise ValueError("El monto pagado es insuficiente para cubrir el total de la factura.")
                
                cambio = monto_pagado - total_final

                # Crear la factura usando el método del modelo
                nueva_factura = Factura.crear_factura(
                    clientes_idclientes,
                    vendedores_idvendedores,
                    datetime.today().date(),
                    datetime.today().time(),
                    total_final,
                    impuesto,
                    descuento,
                    monto_pagado,
                    cambio,
                    db
                )

                if not nueva_factura:
                    flash('Error al crear la factura', 'danger')
                    return redirect(url_for('factura_crear'))

                # Agregar detalles de los productos
                if not DetalleProducto.agregar_detalles(nueva_factura.id, productos, db):
                    flash('Error al agregar productos a la factura', 'danger')
                    return redirect(url_for('factura_crear'))

                flash('Factura creada exitosamente', 'success')
                return redirect(url_for('factura_crear'))

            except Exception as e:
                db.rollback()
                flash(f'Error al crear la factura: {str(e)}', 'danger')

            finally:
                db.close()

        # GET: Cargar datos para el formulario
        try:
            vendedores = Vendedores.obtener_vendedores()
            productos_data = Productos.obtener_productos()
            productos = [
                {
                    "id": producto.Productos.idproductos,
                    "codigo": producto.Productos.codigo,
                    "nombre": producto.Productos.nombre,
                    "descripcion": producto.Productos.descripcion,
                    "categoria": producto.Categoria.nombre,
                    "unidad_medida": producto.UnidadMedida.unidad_medida,
                    "precio_unitario": float(producto.Productos.precio_unitario),
                    "cantidad_stock": producto.Productos.cantidad_stock,
                    "is_active": producto.Productos.is_active
                }
                for producto in productos_data
            ]

        except Exception as e:
            flash(f'Error al cargar los datos: {str(e)}', 'danger')

        return render_template('form_generacion_factura.html', vendedores=vendedores, productos=productos, titulo_pagina="Generar factura")

    #--------------------------

    #Ruta para consultar las facturas

    @app.route('/facturas_por_fecha', methods=['GET'])
    def obtener_facturas_por_fecha():
        fecha = request.args.get('fecha')  # Obtener la fecha de los parámetros de la URL
        
        # Llamar al método en el modelo para buscar facturas por la fecha
        facturas_data = Factura.buscar_por_fecha(fecha)
        
        if facturas_data:
            return jsonify(facturas_data), 200
        else:
            return jsonify({'message': 'No se encontraron facturas para la fecha seleccionada'}), 404
    
    #---------------

    #Ruta para ver el detalle de las facturas
    @app.route('/detalles_factura/<int:id_factura>', methods=['GET'])
    def obtener_detalles_factura(id_factura):
        # Llamar al método en el modelo para obtener los detalles de la factura
        factura_data = Factura.obtener_detalles(id_factura)

        if factura_data:
            return jsonify(factura_data), 200
        else:
            return jsonify({'message': 'Factura no encontrada'}), 404
    
    #-----------------