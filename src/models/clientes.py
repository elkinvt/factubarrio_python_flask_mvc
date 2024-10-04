#crear la tabla de la base de datos!!!
from sqlalchemy import Column, Integer, String, Boolean,ForeignKey
from . import Base

class Clientes(Base):
    __tablename__ = 'clientes'
    
    idclientes = Column(Integer, primary_key=True, autoincrement=True)
    tipo_documento = Column(String(10), nullable=False)
    numero_documento = Column(String(20), unique=True, nullable=False)
    nombres_cliente = Column(String(100), nullable=False)
    telefono = Column(String(15))
    direccion_iddireccion = Column(Integer, ForeignKey('direccion.iddireccion'))  # Relación con la tabla Dirección
    email = Column(String(100))
    is_deleted = Column(Boolean, default=False)  # Campo de eliminación lógica
    is_active = Column(Boolean, default=True)  # Campo de activación

    def __init__(self, tipo_documento, numero_documento, nombres_cliente, telefono, direccion_iddireccion, email):
        self.tipo_documento = tipo_documento
        self.numero_documento = numero_documento
        self.nombres_cliente = nombres_cliente
        self.telefono = telefono
        self.direccion_iddireccion = direccion_iddireccion
        self.email = email

    def __repr__(self):
        return f'<Cliente {self.nombres_cliente}>'
    
    



