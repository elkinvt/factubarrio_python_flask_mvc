#crear la tabla de la base de datos!!!
from sqlalchemy import Column, Integer, String, Boolean,ForeignKey
from . import Base, SessionLocal

class Clientes(Base):
    __tablename__ = 'clientes'
    
    idclientes = Column(Integer, primary_key=True, autoincrement=True)
    tipo_documento = Column(String(10), nullable=False)
    numero_documento = Column(String(20), unique=True, nullable=False)
    nombres_cliente = Column(String(100), nullable=False)
    telefono = Column(String(15))
    direccion = Column(String(255))
    email = Column(String(100))
    is_deleted = Column(Boolean, default=False)  # Campo de eliminación lógica
    is_active = Column(Boolean, default=True)  # Campo de activación

    def __init__(self, tipo_documento, numero_documento, nombres_cliente, telefono, direccion, email, is_active=True, is_deleted=False):
        self.tipo_documento = tipo_documento
        self.numero_documento = numero_documento
        self.nombres_cliente = nombres_cliente
        self.telefono = telefono
        self.direccion = direccion
        self.email = email
        self.is_active = is_active  # Ahora acepta is_active
        self.is_deleted = is_deleted  # Ahora acepta is_deleted

    def __repr__(self):
        return f'<Cliente {self.nombres_cliente}>'
    
    
    # Método estático para obtener los clientes no eliminados
    @staticmethod
    def obtener_clientes():
        session = SessionLocal()
        try:
            clientes = session.query(Clientes).filter_by(is_deleted=False).all()
            return clientes
        finally:
            session.close()


