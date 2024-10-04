from sqlalchemy import Column, Integer, String
from . import Base

class Categoria(Base):
    __tablename__ = 'categoria'
    
    idcategoria = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(50), nullable=False, unique=True)
    
    def __init__(self, nombre):
        self.nombre = nombre

    def __repr__(self):
        return f'<Categoria {self.nombre}>'
