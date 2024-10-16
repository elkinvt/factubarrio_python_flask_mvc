from sqlalchemy import Column, Integer, ForeignKey, Numeric
from sqlalchemy.exc import SQLAlchemyError
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
    
    #Metodo estatico para agregar productos al detalle de la factura
    @classmethod
    def agregar_detalles(cls, factura_id, productos, db_session):
        try:
            for producto in productos:
                detalle = cls(
                    factura_idfactura=factura_id,
                    productos_idproductos=producto['id'],  # Usamos el ID del producto
                    cantidad=producto['cantidad'],
                    precio_unitario=producto['precio'],
                    total_precio=producto['subtotal']
                )
                db_session.add(detalle)
            db_session.commit()
        except SQLAlchemyError as e:
            db_session.rollback()
            print(f"Error al agregar detalles: {str(e)}")
            return False
        return True
    #----------

   