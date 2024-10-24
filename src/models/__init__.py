from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Creación del motor de la base de datos para conectarse con PostgreSQL
engine = create_engine("postgresql+psycopg2://postgres:KDOSQZTR024@localhost/factu_barrio_4")

# Declarative base: esto será usado más adelante para definir los modelos
Base = declarative_base()

# Crear una sesión para interactuar con la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


