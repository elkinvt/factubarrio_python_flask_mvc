from flask import request, redirect, url_for, flash, render_template
from models.detalle_producto import DetalleProducto
from flask import render_template, request, redirect, url_for, flash
from models.clientes import Clientes  # Importar la clase Clientes
from models.vendedores import Vendedores  # Importar la clase Vendedores
from models.productos import Productos  # Importar la clase Productos
from models.facturas import Factura  # Importar la clase Factura
from models.detalle_producto import DetalleProducto  # Importar DetalleProducto
from models import SessionLocal # Importar la sesión para interactuar con la base de datos
from datetime import datetime
import json



def registrar_rutas(app):

    @app.route('/generar_factura', methods=['GET', 'POST'])
    def factura_crear():
        db = SessionLocal()

        if request.method == 'POST':
            try:
                
                # Recibe los datos del formulario
                clientes_idclientes = request.form.get('clienteId')
                vendedores_idvendedores = request.form.get('vendedorFactura')
                productos = json.loads(request.form.get('productosFactura'))

                # Calcular el total de la factura
                total_valor = sum([float(item['precio']) * int(item['cantidad']) for item in productos])
                impuesto = total_valor * 0.19  # Impuesto del 19%
                descuento = float(request.form.get('descuentoFactura', 0))
                total_final = total_valor + impuesto - descuento

                # Crear la factura usando el método del modelo
                nueva_factura = Factura.crear_factura(
                    clientes_idclientes,
                    vendedores_idvendedores,
                    datetime.today().date(),
                    datetime.today().time(),
                    total_final,
                    impuesto,
                    descuento,
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
