from sqlalchemy import Column, Integer, String
from src.models import Base

class Categoria(Base):
    __tablename__ = 'categoria'
    
    idcategoria = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(50), nullable=False, unique=True)
    
    def __init__(self, nombre):
        self.nombre = nombre

    def __repr__(self):
        return f'<Categoria {self.nombre}>'
    
    
    #Metodo estatico para obtener las categorias
    @staticmethod
    def obtener_todas(db_session):
        try:
            categorias = db_session.query(Categoria).all()
            return categorias
        except Exception as e:
            raise e
    #-------------------