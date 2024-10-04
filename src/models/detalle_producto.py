from sqlalchemy import Column, Integer, ForeignKey, Numeric
from . import Base

class DetalleProducto(Base):
    __tablename__ = 'detalle_producto'
    
    factura_idfactura = Column(Integer, ForeignKey('factura.id'), primary_key=True)
    productos_idproductos = Column(Integer, ForeignKey('productos.idproductos'), primary_key=True)
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(Numeric(10, 2), nullable=False)
    total_precio = Column(Numeric(10, 2), nullable=False)

    def __init__(self, factura_idfactura, productos_idproductos, cantidad, precio_unitario, total_precio):
        self.factura_idfactura = factura_idfactura
        self.productos_idproductos = productos_idproductos
        self.cantidad = cantidad
        self.precio_unitario = precio_unitario
        self.total_precio = total_precio

    def __repr__(self):
        return f'<DetalleProducto Factura {self.factura_id} Producto {self.productos_idproductos}>'
