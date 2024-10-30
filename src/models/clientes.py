from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.exc import SQLAlchemyError
from contextlib import contextmanager
from src.models import Base, SessionLocal, db_session_manager

class Clientes(Base):
    __tablename__ = 'clientes'
    
    idclientes = Column(Integer, primary_key=True, autoincrement=True)
    tipo_documento = Column(String(10), nullable=False)
    numero_documento = Column(String(20), unique=True, nullable=False)
    nombres_cliente = Column(String(100), nullable=False)
    telefono = Column(String(15))
    direccion = Column(String(255))
    email = Column(String(100))
    is_deleted = Column(Boolean, default=False)  # Campo de eliminación lógica
    is_active = Column(Boolean, default=True)  # Campo de activación

    def __init__(self, tipo_documento, numero_documento, nombres_cliente, telefono, direccion, email, is_active=True, is_deleted=False):
        self.tipo_documento = tipo_documento
        self.numero_documento = numero_documento
        self.nombres_cliente = nombres_cliente
        self.telefono = telefono
        self.direccion = direccion
        self.email = email
        self.is_active = is_active  # Ahora acepta is_active
        self.is_deleted = is_deleted  # Ahora acepta is_deleted

    def __repr__(self):
        return f'<Cliente {self.nombres_cliente}>'
    
    
    # Contexto de sesión para gestionar apertura y cierre automáticamente
    @staticmethod
    @contextmanager
    def session_scope():
        session = SessionLocal()
        try:
            yield session
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Database error: {e}")
            raise e
        finally:
            session.close()

   
    # Método para obtener los clientes no eliminados
    @staticmethod
    def obtener_clientes():
        """Obtener todos los clientes no eliminados."""
        return SessionLocal.query(Clientes).filter_by(is_deleted=False).all()
    
    #--------

    # Método estático para agregar un cliente      
    @staticmethod
    def agregar_cliente(cliente):
        with db_session_manager() as session:
            session.add(cliente)
            session.commit()  # Confirma los cambios
            return cliente
    
    #----------

    # Método estático para buscar un cliente usando una sesión existente
    @staticmethod
    def buscar_cliente_por_documento(tipo_documento, numero_documento):
        return SessionLocal.query(Clientes).filter_by(
            tipo_documento=tipo_documento, numero_documento=numero_documento
        ).first()

    #---------


    # Método estático para actualizar un vendedor     
    @staticmethod
    def actualizar_cliente(cliente_id, datos_actualizados):
        with db_session_manager() as session:
            cliente = session.query(Clientes).filter_by(idclientes=cliente_id).first()

            if not cliente:
                raise ValueError("Vendedor no encontrado")

            # Actualizar los datos
            for key, value in datos_actualizados.items():
                setattr(cliente, key, value)

            session.commit()  # Confirma los cambios en la base de datos
            return cliente
    #--------------

    # Método estático para actualizar estado del cliente 
    @staticmethod
    def actualizar_estado(db_session, cliente):
        """Toggle de estado de cliente"""
        cliente.is_active = not cliente.is_active
        db_session.add(cliente)
        return cliente
    #--------

    # Método estático para eliminar un cliente 
    @staticmethod
    def eliminar_cliente_logicamente(cliente):
        with db_session_manager() as session:
            cliente.is_deleted = True
            session.commit()
    #--------

    # Método estático para buscar el cliente en la factura
    @staticmethod
    def buscar_por_numero_documento(query):
        """Búsqueda parcial por número de documento"""
        with Clientes.session_scope() as session:
            return [{
                'id': cliente.idclientes,
                'nombre': cliente.nombres_cliente,
                'numero_documento': cliente.numero_documento,
                'direccion': cliente.direccion,
                'telefono': cliente.telefono,
                'is_active': cliente.is_active
            } for cliente in session.query(Clientes)
                .filter(Clientes.numero_documento.ilike(f"%{query}%"))
                .all()]
    #-----------

    # Método estático para validar duplicaciones del cliente
    @staticmethod
    def validar_datos(numero_documento=None, email=None):
        """Validar unicidad de documento y email"""
        errores = {}
        with Clientes.session_scope() as session:
            if numero_documento and session.query(Clientes).filter_by(numero_documento=numero_documento).first():
                errores['numeroDocumento'] = 'Este número de documento ya está registrado.'
            if email and session.query(Clientes).filter_by(email=email).first():
                errores['emailCliente'] = 'Este correo electrónico ya está registrado.'
        return errores
    #--------

