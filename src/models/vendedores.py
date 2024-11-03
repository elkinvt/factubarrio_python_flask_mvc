from sqlalchemy import Column, Integer, String, Boolean
from src.models import Base, db_session_manager, to_dict

class Vendedores(Base):
    __tablename__ = 'vendedores'
    
    idvendedores = Column(Integer, primary_key=True, autoincrement=True)
    tipo_documento = Column(String(10), nullable=False)
    numero_documento = Column(String(20), unique=True, nullable=False)
    nombres_vendedor = Column(String(100), nullable=False)
    telefono = Column(String(15))
    direccion = Column(String(255))  
    email = Column(String(100))
    is_deleted = Column(Boolean, default=False)  # Campo de eliminación lógica

    def __init__(self, tipo_documento, numero_documento, nombres_vendedor, telefono, direccion, email, is_deleted=False):
        self.tipo_documento = tipo_documento
        self.numero_documento = numero_documento
        self.nombres_vendedor = nombres_vendedor
        self.telefono = telefono
        self.direccion = direccion
        self.email = email
        self.is_deleted = is_deleted  # Ahora acepta is_deleted

    def __repr__(self):
        return f'<Vendedor {self.nombres_vendedor}>'
    
    
   # Método para obtener los vendedores no eliminados
    @staticmethod
    def obtener_vendedores():
        with db_session_manager() as session:
            vendedores = session.query(Vendedores).filter_by(is_deleted=False).all()
            return [to_dict(vendedor) for vendedor in vendedores]

    #------------     

    # Método estático para agregar un vendedor      
    @staticmethod
    def agregar_vendedor(vendedor):
        with db_session_manager() as session:
            session.add(vendedor)
            session.commit()  # Confirma los cambios
            return vendedor
    #------------------
    
    # Método estático para buscar un vendedor usando una sesión existente
    @staticmethod
    def buscar_vendedor_por_documento(tipo_documento, numero_documento):
        with db_session_manager() as session:
            vendedor = session.query(Vendedores).filter_by(
            tipo_documento=tipo_documento, numero_documento=numero_documento).first()

            return to_dict(vendedor) if vendedor else None

    #---------
    
    # Método estático para actualizar un vendedor     
    @staticmethod
    def actualizar_vendedor(vendedor_id, datos_actualizados):
        with db_session_manager() as session:
            vendedor = session.query(Vendedores).filter_by(idvendedores=vendedor_id).first()

            if not vendedor:
                raise ValueError("Vendedor no encontrado")

            # Actualizar los datos
            for key, value in datos_actualizados.items():
                setattr(vendedor, key, value)

            session.commit()  # Confirma los cambios en la base de datos
            return vendedor
    #--------------

    #Metodo estatico para buscar vendedor por id
    @staticmethod
    def buscar_vendedor_por_id(vendedor_id):
        with db_session_manager() as session:
            return session.query(Vendedores).filter_by(idvendedores=vendedor_id).first()
    
    #-----------------
    
    # Método estático para eliminar un vendedor 
    @staticmethod
    def eliminar_vendedor_logicamente(tipo_documento, numero_documento):
        with db_session_manager() as session:
            vendedor = session.query(Vendedores).filter_by(tipo_documento=tipo_documento, numero_documento=numero_documento). first()
            vendedor.is_deleted = True  # Marcamos el vendedor como eliminado
            session.commit()  # Guardamos los cambios en la base de datos
            return True
        return False

    #------------    

    # Método de validación en Vendedores
    @staticmethod
    def validar_datos(numero_documento=None, email=None):
        with db_session_manager() as session:
            errores = {}
            if numero_documento and session.query(Vendedores).filter_by(numero_documento=numero_documento).first():
                errores['numeroDocumento'] = 'Este número de documento ya está registrado.'
            if email and session.query(Vendedores).filter_by(email=email).first():
                errores['emailVendedor'] = 'Este correo electrónico ya está registrado.'
            return errores

    #---------

    

