from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from sqlalchemy.inspection import inspect

# Creación del motor de la base de datos para conectarse con PostgreSQL
engine = create_engine("postgresql+psycopg2://postgres:KDOSQZTR024@localhost/factu_barrio_6")

# Declarative base: esto será usado más adelante para definir los modelos
Base = declarative_base()

# Crear una sesión para interactuar con la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Contexto de sesión para gestionar apertura y cierre automáticamente
@contextmanager
def db_session_manager():
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()
        
#-------------

#Convierte cualquier objeto SQLAlchemy en un diccionario.
def to_dict(obj):
    """Convierte cualquier objeto SQLAlchemy en un diccionario."""
    try:
        result = {c.key: getattr(obj, c.key) for c in inspect(obj).mapper.column_attrs}
        #print("Resultado de to_dict:", result)  # Imprime el resultado de cada conversión
        return result
    except KeyError as e:
        print(f"KeyError en to_dict: {e}")
        raise

#------------