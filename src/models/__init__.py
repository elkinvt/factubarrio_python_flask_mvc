from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Reemplaza 'usuario', 'contraseña', y 'factu_barrio' con tus credenciales y nombre de base de datos
DATABASE_URL = "postgresql+psycopg2://postgres:KDOSqztr024**@localhost/factu_barrio_4"

# Creación del motor de la base de datos para conectarse con PostgreSQL
engine = create_engine(DATABASE_URL)

# Declarative base: esto será usado más adelante para definir los modelos
Base = declarative_base()

# Crear una sesión para interactuar con la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Función para inicializar las tablas
def init_db():
    from src.models.categorias import Categoria
    from src.models.unidad_medida import UnidadMedida
    from src.models.clientes import Clientes  
    from src.models.facturas import Factura
    from src.models.vendedores import Vendedores
    from src.models.productos import Productos
    from src.models.detalle_producto import DetalleProducto
    
    # Crear todas las tablas
    Base.metadata.create_all(bind=engine)

#--------------
