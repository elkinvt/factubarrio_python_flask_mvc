from flask import Flask
from src.models import Base, engine  # Importar la base y el engine para crear las tablas
from flask_controller import FlaskControllerRegister #importar la libreria de los controladores
from sqlalchemy import inspect

app = Flask(__name__)

app.secret_key = 'supersecreta'  # Necesaria para manejar los mensajes flash



register = FlaskControllerRegister(app)
register.register_package('src.controllers')

print("Tablas registradas para crear:", Base.metadata.tables.keys())

# Crear todas las tablas
Base.metadata.create_all(bind=engine)

# Inspeccionar las tablas que se han creado
inspector = inspect(engine)
print("Tablas creadas:", inspector.get_table_names())



# Punto de entrada de la aplicación
if __name__ == '__main__':
    app.run(debug=True)