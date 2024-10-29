from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.exc import SQLAlchemyError
from contextlib import contextmanager
from src.models import Base, SessionLocal

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

    # Métodos CRUD
    @staticmethod
    def crear_o_actualizar(db_session, cliente, datos_actualizados=None):
        """Método genérico para crear o actualizar cliente"""
        if datos_actualizados:
            for key, value in datos_actualizados.items():
                setattr(cliente, key, value)
        db_session.add(cliente)
        return cliente

    @staticmethod
    def obtener_clientes():
        """Obtener todos los clientes no eliminados y convertirlos a diccionarios"""
        with Clientes.session_scope() as session:
            clientes = session.query(Clientes).filter_by(is_deleted=False).all()
            # Convertir los objetos Cliente a diccionarios
            return [{
                'idclientes': cliente.idclientes,
                'tipo_documento': cliente.tipo_documento,
                'numero_documento': cliente.numero_documento,
                'nombres_cliente': cliente.nombres_cliente,
                'telefono': cliente.telefono,
                'direccion': cliente.direccion,
                'email': cliente.email,
                'is_active': cliente.is_active
            } for cliente in clientes]


    
    @staticmethod
    def buscar_cliente_como_diccionario(**kwargs):
        """Buscar cliente y devolverlo como un diccionario para mostrar en la vista"""
        with Clientes.session_scope() as session:
            cliente = session.query(Clientes).filter_by(**kwargs).first()
            if cliente:
                return {
                    'idclientes': cliente.idclientes,
                    'tipo_documento': cliente.tipo_documento,
                    'numero_documento': cliente.numero_documento,
                    'nombres_cliente': cliente.nombres_cliente,
                    'telefono': cliente.telefono,
                    'direccion': cliente.direccion,
                    'email': cliente.email,
                    'is_active': cliente.is_active,
                    'is_deleted': cliente.is_deleted
                }
            return None
        
    @staticmethod
    def buscar_cliente(**kwargs):
        """Buscar cliente y devolver la instancia del modelo para manipulación directa"""
        with Clientes.session_scope() as session:
            return session.query(Clientes).filter_by(**kwargs).first()


    @staticmethod
    def actualizar_estado(db_session, cliente):
        """Toggle de estado de cliente"""
        cliente.is_active = not cliente.is_active
        db_session.add(cliente)
        return cliente

    @staticmethod
    def eliminar_cliente_logicamente(db_session, cliente):
        """Eliminar cliente lógicamente"""
        cliente.is_deleted = True
        db_session.add(cliente)
        return cliente

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

