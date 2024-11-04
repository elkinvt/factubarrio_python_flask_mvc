from sqlalchemy import Column, Integer, String, Boolean
from src.models import Base, db_session_manager, to_dict

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
        self.nombres_usuario = nombre_usuario
        self.email = email
        self.contraseña = contraseña
        self.rol = rol
        self.is_active = is_active 
        self.is_deleted = is_deleted  

    def __repr__(self):
            return f'<Usuario {self.nombres_usuario}>'
    
    # Método para obtener los usuarios no eliminados
    @staticmethod
    def obtener_usuarios():
        with db_session_manager() as session:
            usuarios = session.query(Usuarios).filter_by(is_deleted=False).all()
            return [to_dict(usuario) for usuario in usuarios]

    #------------ 

    # Método estático para agregar un usuario      
    @staticmethod
    def agregar_usuario(usuario):
        with db_session_manager() as session:
            session.add(usuario)
            session.commit()  # Confirma los cambios
            return usuario
    #------------------