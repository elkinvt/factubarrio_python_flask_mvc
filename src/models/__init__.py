from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Reemplaza 'usuario', 'contraseña', y 'factu_barrio' con tus credenciales y nombre de base de datos
DATABASE_URL = "postgresql+psycopg2://postgres:KDOSqztr024**@localhost/factu_barrio_2"

# Creación del motor de la base de datos para conectarse con PostgreSQL
engine = create_engine(DATABASE_URL)

# Declarative base: esto será usado más adelante para definir los modelos
Base = declarative_base()

# Crear una sesión para interactuar con la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Función para inicializar las tablas
def init_db():
    from .direcciones import Direccion
    from .detalle_producto import DetalleProducto
    from .categorias import Categoria
    from .unidad_medida import UnidadMedida
    from .clientes import Clientes  # Importa los modelos que necesites
    from .facturas import Factura
    from .vendedores import Vendedores
    from .productos import Productos
    from .detalle_producto import DetalleProducto
    from .facturas import Factura
   
    
     # Crear todas las tablas
    Base.metadata.create_all(bind=engine)
