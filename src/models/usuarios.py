from sqlalchemy import Column, Integer, String, Boolean
from src.models import  Base, db_session_manager, to_dict
from sqlalchemy import func
from src.models.vendedores import Vendedores

class Usuarios(Base):
    __tablename__ = 'usuarios'

    id_usuario = Column(Integer, primary_key=True, autoincrement=True)
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

    # Método estático para buscar usuario por nombre
    @staticmethod
    def buscar_usuario_por_nombre(nombre_usuario):
        with db_session_manager() as session:
            usuario =session.query(Usuarios).filter(func.lower(Usuarios.nombres_usuario)==nombre_usuario.lower().strip()).first()
            return to_dict(usuario) if usuario else None

    #-----------------

    # Método estático para actualizar un usuario     
    @staticmethod
    def actualizar_usuario(usuario_id, datos_actualizados):
        with db_session_manager() as session:

            usuario = session.query(Usuarios).filter_by(id_usuario=usuario_id).first()
            


            if not usuario:
                raise ValueError("usuario no encontrado")

            # Actualizar los datos
            for key, value in datos_actualizados.items():
                setattr(usuario, key, value)

            session.commit()  # Confirma los cambios en la base de datos
            return usuario
    #--------------

     # Método estático para actualizar estado del usuario
    @staticmethod
    def actualizar_estado(nombres_usuario):
        """Toggle de estado de usuario"""
        with db_session_manager() as session:
            usuario = session.query(Usuarios).filter_by(nombres_usuario=nombres_usuario).first()
            
            if usuario:
                 # Cambiar el estado activo/inactivo
                usuario.is_active = not usuario.is_active
                session.commit()
            return usuario.is_active
        return None
    #--------

    # Método estático para eliminar un cliente 
    @staticmethod
    def eliminar_usuario_logicamente(nombres_usuario):

        with db_session_manager() as session:
            
            usuario = session.query(Usuarios).filter(func.lower(Usuarios.nombres_usuario) == nombres_usuario.lower()).first()
            
            if usuario and not usuario.is_deleted:
                usuario.is_deleted = True
                session.commit()
                return True
            return False
        
    #------------

    
    # Método de validación en Usuarios
    @staticmethod
    def validar_datos(email=None, usuario_id=None):
        with db_session_manager() as session:
            errores = {}

            # Validar duplicado de email solo en Usuarios, excluyendo el usuario actual si usuario_id está presente
            if email:
                usuario_email = session.query(Usuarios).filter_by(email=email).first()
                if usuario_email and (usuario_id is None or usuario_email.id_usuario != int(usuario_id)):
                    errores['emailUsuario'] = 'Este correo electrónico ya está registrado en Usuarios.'

            return errores
        
    #--------------

