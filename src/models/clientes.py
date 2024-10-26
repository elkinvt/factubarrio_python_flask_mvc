#crear la tabla de la base de datos!!!
from sqlalchemy import Column, Integer, String, Boolean
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
    
    
    # Método estático para obtener los clientes no eliminados
    @staticmethod
    def obtener_clientes():
        session = SessionLocal()
        try:
            clientes = session.query(Clientes).filter_by(is_deleted=False).all()
            return clientes
        finally:
            session.close()
    #------------        
    
    # Método estático para agregar un cliente       
    @staticmethod
    def agregar_cliente(db_session, cliente):
        try:
            db_session.add(cliente)
            db_session.commit()
            return cliente
        except Exception as e:
            db_session.rollback()
            raise e
    #------------------
        
        
    # Método estático para buscar un cliente usando una sesión existente
    @staticmethod
    def buscar_cliente_por_documento(db_session, tipo_documento, numero_documento):
        cliente = db_session.query(Clientes).filter_by(
            tipo_documento=tipo_documento,
            numero_documento=numero_documento
        ).first()
        return cliente

    #------------- 
    
    # Método estático para actualizar un cliente       
    @staticmethod
    def actualizar_cliente(db_session, cliente, datos_actualizados):
        try:
            for key, value in datos_actualizados.items():
                setattr(cliente, key, value)
            db_session.commit()
            return cliente
        except Exception as e:
            db_session.rollback()
            raise e
    @staticmethod
    def buscar_cliente_por_id(cliente_id):
        session = SessionLocal()
        try:
            cliente = session.query(Clientes).filter_by(idclientes=cliente_id).first()
            return cliente
        finally:
            session.close()
            
    #-----------------
            
    # Método estático para actualizar el estado de un cliente        
    @staticmethod
    def toggle_estado_cliente(db_session, cliente):
        try:
            cliente.is_active = not cliente.is_active  # Cambia el estado (activo/inactivo)
            db_session.commit()  # Guarda los cambios en la base de dato
            return cliente
        except Exception as e:
            db_session.rollback()  # Revierte los cambios si hay algún error
            raise e
    #-----------
    
    #Metodo para eliminar cliente(eliminacion logica)
    @staticmethod
    def eliminar_cliente(db_session, cliente):
        try:
            cliente.is_deleted = True  # Marcamos el cliente como eliminado
            db_session.commit()  # Guardamos los cambios
        except Exception as e:
            db_session.rollback()  # En caso de error, revertimos la transacción
            raise e
    #------------

    # Método para buscar clientes por número de documento
    @staticmethod
    def buscar_por_numero_documento(query):
        db = SessionLocal()
        try:
            # Consulta para buscar clientes cuyo número de documento coincida parcialmente con 'query'
            clientes = db.query(Clientes).filter(
                Clientes.numero_documento.ilike(f"%{query}%")
            ).all()

            # Serializar los datos del cliente incluyendo el estado de actividad
            return [{
                'id': cliente.idclientes,
                'nombre': cliente.nombres_cliente,
                'numero_documento': cliente.numero_documento,
                'direccion': cliente.direccion,
                'telefono': cliente.telefono,
                'is_active': cliente.is_active  # Añadir estado de actividad
            } for cliente in clientes]
        except Exception as e:
            print(f"Error al buscar clientes: {e}")
            return {'error': 'Error al buscar clientes'}
        finally:
            db.close()

    #--------------





    # Método para verificar si un cliente está inactivo.
    @staticmethod
    def verificar_cliente_inactivo(numero_documento):
        # Crea una sesión de base de datos
        db = SessionLocal()
        try:
            # Buscar el cliente por número de documento
            cliente = db.query(Clientes).filter_by(numero_documento=numero_documento).first()

            if cliente:
                if not cliente.is_active:
                    return {'inactivo': True}
                else:
                    return {'existe': True, 'nombre': cliente.nombre_completo, 'id': cliente.idclientes}
            else:
                return {'existe': False}
        except Exception as e:
            print(f"Error al verificar cliente: {e}")
            return {'error': 'Error al verificar el cliente'}
        finally:
            db.close()
