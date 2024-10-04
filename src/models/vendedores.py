from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from . import Base

class Vendedores(Base):
    __tablename__ = 'vendedores'
    
    idvendedores = Column(Integer, primary_key=True, autoincrement=True)
    tipo_documento = Column(String(10), nullable=False)
    numero_documento = Column(String(20), unique=True, nullable=False)
    nombres_vendedor = Column(String(100), nullable=False)
    telefono = Column(String(15))
    direccion_iddireccion = Column(Integer, ForeignKey('direccion.iddireccion'))  # Relación con la tabla Dirección
    email = Column(String(100))
    is_deleted = Column(Boolean, default=False)  # Campo de eliminación lógica

    def __init__(self, tipo_documento, numero_documento, nombres_vendedor, telefono, direccion_iddireccion, email):
        self.tipo_documento = tipo_documento
        self.numero_documento = numero_documento
        self.nombres_vendedor = nombres_vendedor
        self.telefono = telefono
        self.direccion_iddireccion = direccion_iddireccion
        self.email = email

    def __repr__(self):
        return f'<Vendedor {self.nombres_vendedor}>'



