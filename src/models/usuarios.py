from sqlalchemy import Column, Integer, String, Boolean
from src.models import Base

class Usuarios(Base):
    __tablename__ = 'usuarios'

    id_usuarios = Column(Integer, primary_key=True, autoincrement=True)
    nombres_usuario = Column(String(100), nullable=False)
    email = Column(String(100),nullable=False, unique=True)
    contraseña = Column(String(128),nullable=False)
    rol = Column(String(100),nullable=False)
    is_deleted = Column(Boolean, default=False) 
    is_active = Column(Boolean, default=True)  # Campo de activación

    def __init__(self,nombre_usuario, email, contraseña, rol,is_active=True, is_deleted=False):
        print(f"Creando instancia de Usuarios: {nombre_usuario}, {email}")
        self.nombres_usuario = nombre_usuario
        self.email = email
        self.contraseña = contraseña
        self.rol = rol
        self.is_active = is_active 
        self.is_deleted = is_deleted  

    def __repr__(self):
            return f'<Usuario {self.nombres_usuario}>'