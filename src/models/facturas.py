from sqlalchemy import Column, Integer, ForeignKey, Date, Time, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.exc import SQLAlchemyError

from . import Base

class Factura(Base):
    __tablename__ = 'factura'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    clientes_idclientes = Column(Integer, ForeignKey('clientes.idclientes'), nullable=False)  # Apunta correctamente a 'idclientes'
    vendedores_idvendedores = Column(Integer, ForeignKey('vendedores.idvendedores'), nullable=False)  # Apunta correctamente a 'idvendedores'
    fecha = Column(Date, nullable=False)
    hora = Column(Time, nullable=False)
    total_valor = Column(Numeric(10, 2), nullable=False)
    impuesto = Column(Numeric(10, 2), nullable=False)
    descuento = Column(Numeric(10, 2), nullable=True)
    monto_pagado = Column(Numeric(10, 2), nullable=False)
    cambio = Column(Numeric(10, 2), nullable=True)

    # Relación con el cliente
    cliente = relationship('Clientes', backref='facturas')

    # Relación con el vendedor
    vendedor = relationship('Vendedores', backref='facturas')

    #Relacion con detalle_producto
    detalles = relationship('DetalleProducto', backref='factura')

    def __init__(self, clientes_idclientes, vendedores_idvendedores, fecha, hora, total_valor, impuesto, descuento=None, monto_pagado=None, cambio=None):
        self.clientes_idclientes = clientes_idclientes
        self.vendedores_idvendedores = vendedores_idvendedores
        self.fecha = fecha
        self.hora = hora
        self.total_valor = total_valor
        self.impuesto = impuesto
        self.descuento = descuento
        self.monto_pagado = monto_pagado
        self.cambio = cambio

    def __repr__(self):
        return f'<Factura {self.id}>'
    
    # Método para crear una factura
    @classmethod
    def crear_factura(cls, clientes_idclientes, vendedores_idvendedores, fecha, hora, total_valor, impuesto, descuento, monto_pagado, cambio , db_session):
        try:
            nueva_factura = cls(
                clientes_idclientes=clientes_idclientes,
                vendedores_idvendedores=vendedores_idvendedores,
                fecha=fecha,
                hora=hora,
                total_valor=total_valor,
                impuesto=impuesto,
                descuento=descuento,
                monto_pagado=monto_pagado,
                cambio=cambio
            )
            db_session.add(nueva_factura)
            db_session.commit()
            return nueva_factura
        except SQLAlchemyError as e:
            db_session.rollback()
            print(f"Error al crear la factura: {str(e)}")
            return None
    #--------------------------
     
