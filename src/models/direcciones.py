from sqlalchemy import Column, Integer, String
from . import Base

class Direccion(Base):
    __tablename__ = 'direccion'
    
    iddireccion = Column(Integer, primary_key=True, autoincrement=True)
    tipo_via = Column(String(20), nullable=False)
    numero_via = Column(Integer, nullable=False)
    letra_bis = Column(String(2))
    numero_via_secundaria = Column(Integer, nullable=False)
    numero_placa = Column(Integer, nullable=False)
    detalles_adicionales = Column(String(100))
    barrio = Column(String(50), nullable=False, default="desconocido")
    ciudad = Column(String(50), nullable=False, default="desconocido")
    municipio = Column(String(50), nullable=False, default="desconocido")
    pais = Column(String(50), nullable=False, default="desconocido")

    def __init__(self, tipo_via, numero_via, letra_bis, numero_via_secundaria, numero_placa, detalles_adicionales, barrio, ciudad, municipio, pais):
        self.tipo_via = tipo_via
        self.numero_via = numero_via
        self.letra_bis = letra_bis
        self.numero_via_secundaria = numero_via_secundaria
        self.numero_placa = numero_placa
        self.detalles_adicionales = detalles_adicionales
        self.barrio = barrio
        self.ciudad = ciudad
        self.municipio = municipio
        self.pais = pais

    def __repr__(self):
        return f'<Direccion {self.tipo_via} {self.numero_via}-{self.numero_via_secundaria}>'
