from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.models import Base, SessionLocal

class UnidadMedida(Base):
    __tablename__ = 'unidad_medida'
    
    idunidad_medida = Column(Integer, primary_key=True, autoincrement=True)
    unidad_medida = Column(String(20), nullable=False, unique=True)
    unidad_padre_id = Column(Integer, ForeignKey('unidad_medida.idunidad_medida'))  # Clave foránea hacia sí misma

    # Relación para acceder a la unidad padre desde una unidad hija
    unidad_padre = relationship('UnidadMedida', remote_side=[idunidad_medida], backref='subunidades')

    def __init__(self, unidad_medida, unidad_padre_id=None):
        self.unidad_medida = unidad_medida
        self.unidad_padre_id = unidad_padre_id

    def __repr__(self):
        return f'<UnidadMedida {self.unidad_medida}>'


    #Metodo estatico para obtener las unidades de medida
    @staticmethod
    def obtener_todas_con_subunidades():
        session = SessionLocal()
        try:
            unidades_padre = session.query(UnidadMedida).filter(UnidadMedida.unidad_padre_id == None).all()
            subunidades = session.query(UnidadMedida).filter(UnidadMedida.unidad_padre_id != None).all()
            return unidades_padre, subunidades
        except Exception as e:
            raise e
        
        finally:
            session.close()
    #------------------