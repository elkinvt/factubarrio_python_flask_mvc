from sqlalchemy import Column, Integer, String, Numeric, ForeignKey
from . import Base

class Productos(Base):
    __tablename__ = 'productos'
    
    idproductos = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(String(255))
    categoria_idcategoria = Column(Integer, ForeignKey('categoria.idcategoria'), nullable=False)
    unidad_medida_idunidad_medida = Column(Integer, ForeignKey('unidad_medida.idunidad_medida'))
    presentacion = Column(String(50))
    cantidad_stock = Column(Integer, nullable=False)
    precio_unitario = Column(Numeric(10, 2), nullable=False)

    def __init__(self, nombre, descripcion, categoria_idcategoria, unidad_medida_idunidad_medida, presentacion, cantidad_stock, precio_unitario):
        self.nombre = nombre
        self.descripcion = descripcion
        self.categoria_idcategoria = categoria_idcategoria
        self.unidad_medida_idunidad_medida = unidad_medida_idunidad_medida
        self.presentacion = presentacion
        self.cantidad_stock = cantidad_stock
        self.precio_unitario = precio_unitario

    def __repr__(self):
        return f'<Producto {self.nombre}>'


from flask import Blueprint, request, redirect, url_for, flash, render_template, jsonify
from models import SessionLocal  # Asegúrate de que 'SessionLocal' está correctamente importado
from models.productos import Productos  # Importa el modelo Productos

# Definir el blueprint para productos
productos_bp = Blueprint('productos', __name__)

# Aquí puedes continuar con la definición de tus rutas, por ejemplo:
@productos_bp.route('/productos_crear', methods=['GET', 'POST'])
def crear_producto():
    if request.method == 'POST':
        db = SessionLocal()

        # Recibir los datos enviados desde el formulario
        codigo = request.form['codigoProducto']
        nombre = request.form['nombreProducto']
        descripcion = request.form['descripcionProducto']
        categoria = request.form['categoriaProducto']
        precio = request.form['precioProducto']
        unidad_medida = request.form['unidadMedidaProducto']
        presentacion = request.form['presentacionProducto']
        cantidad_stock = request.form['cantidadStockProducto']

        # Crear una nueva instancia del producto
        nuevo_producto = Productos(
            codigo=codigo,
            nombre=nombre,
            descripcion=descripcion,
            categoria=categoria,
            precio=precio,
            unidad_medida=unidad_medida,
            presentacion=presentacion,
            cantidad_stock=cantidad_stock
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

        return redirect(url_for('productos.crear_producto'))

    return render_template('form_crear_producto.html', titulo_pagina="Crear Producto")

# Define más rutas para la gestión de productos, si es necesario
