from sqlalchemy import Column, Integer, String, Numeric,Boolean, ForeignKey
from src.models import Base, SessionLocal
from src.models.categorias import Categoria
from src.models.unidad_medida import UnidadMedida

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
    
    
    # Método estático para obtener los productos no eliminados con JOIN a categorías y unidades de medida
    @staticmethod
    def obtener_productos():
        session = SessionLocal()
        try:
            # Realizamos el join entre productos, categorías y unidades de medida
            productos = session.query(Productos, Categoria, UnidadMedida).join(
                Categoria, Productos.categoria_idcategoria == Categoria.idcategoria  # Join con Categorías
            ).join(
                UnidadMedida, Productos.unidad_medida_idunidad_medida == UnidadMedida.idunidad_medida  # Join con Unidades de Medida
            ).filter(Productos.is_deleted == False).all()  # Filtramos solo productos no eliminados
            
            return productos  # Retornamos la lista de productos con las relaciones
        finally:
            session.close()  # Cerramos la sesión después de completar la consulta

    #------------
    
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

    # Método para buscar productos por código o nombre
    @staticmethod
    def buscar_por_codigo_o_nombre(termino, db_session):
        try:
            productos = db_session.query(Productos).filter(
                (Productos.codigo.ilike(f'%{termino}%')) |
                (Productos.nombre.ilike(f'%{termino}%')),
                Productos.is_deleted == False
            ).all()
            return productos
        except Exception as e:
            raise e
    #---------
    
    # Método para obtener un producto por su ID
    @staticmethod
    def obtener_por_id(id, db_session):
        try:
            producto = db_session.query(Productos).filter_by(idproductos=id, is_deleted=False).first()
            return producto
        except Exception as e:
            raise e
        
    #-----------
    
    # Método para actualizar los datos de un producto
    @staticmethod
    def actualizar_producto(producto, datos_actualizados, db_session):
        try:
            for key, value in datos_actualizados.items():
                setattr(producto, key, value)
            db_session.commit()
            return producto
        except Exception as e:
            db_session.rollback()
            raise e
    
    #-------------


    

