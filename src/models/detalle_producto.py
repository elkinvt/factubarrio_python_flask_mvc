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
    
    #Metodo estatico para agregar productos a la factura
    @staticmethod
    def agregar_detalles(factura_id, productos, db_session):
        try:
            for item in productos:
                nuevo_detalle = DetalleProducto(
                    factura_idfactura=factura_id,
                    productos_idproductos=item['id'],
                    cantidad=item['cantidad'],
                    precio_unitario=item['precio'],
                    total_precio=float(item['precio']) * int(item['cantidad'])
                )
                db_session.add(nuevo_detalle)
            db_session.commit()
        except Exception as e:
            db_session.rollback()
            raise e
    #----------