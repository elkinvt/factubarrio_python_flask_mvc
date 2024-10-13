from sqlalchemy import Column, Integer, String, Numeric,Boolean, ForeignKey
from . import Base

class Productos(Base):
    __tablename__ = 'productos'
    
    idproductos = Column(Integer, primary_key=True, autoincrement=True)
    codigo = Column(String(50), unique=True, nullable=False)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(String(255))
    categoria_idcategoria = Column(Integer, ForeignKey('categoria.idcategoria'), nullable=False)
    unidad_medida_idunidad_medida = Column(Integer, ForeignKey('unidad_medida.idunidad_medida'))
    presentacion = Column(String(50))
    cantidad_stock = Column(Integer, nullable=False)
    precio_unitario = Column(Numeric(10, 2), nullable=False)
    is_deleted = Column(Boolean, default=False)  # Campo de eliminación lógica
    is_active = Column(Boolean, default=True)  # Campo de activación

    def __init__(self, codigo, nombre, descripcion, categoria_idcategoria, unidad_medida_idunidad_medida, presentacion, cantidad_stock, precio_unitario):
        self.codigo = codigo
        self.nombre = nombre
        self.descripcion = descripcion
        self.categoria_idcategoria = categoria_idcategoria
        self.unidad_medida_idunidad_medida = unidad_medida_idunidad_medida
        self.presentacion = presentacion
        self.cantidad_stock = cantidad_stock
        self.precio_unitario = precio_unitario

    def __repr__(self):
        return f'<Producto {self.nombre}>'
    
    
    # Método estático para agregar un producto
    @staticmethod
    def agregar_producto(db_session, producto):
        try:
            db_session.add(producto)
            db_session.commit()
            return producto
        except Exception as e:
            db_session.rollback()
            raise e
    #--------


