from sqlalchemy import Column, Integer, ForeignKey, Date, Time, Numeric
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

    def __init__(self, clientes_idclientes, vendedores_idvendedores, fecha, hora, total_valor, impuesto, descuento=None):
        self.clientes_idclientes = clientes_idclientes
        self.vendedores_idvendedores = vendedores_idvendedores
        self.fecha = fecha
        self.hora = hora
        self.total_valor = total_valor
        self.impuesto = impuesto
        self.descuento = descuento

    def __repr__(self):
        return f'<Factura {self.id}>'

