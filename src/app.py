from flask import Flask
from src.models import Base, engine  # Importar la base y el engine para crear las tablas
from src.models import init_db  # Importar la función init_db para crear las tablas
from flask_controller import FlaskControllerRegister #importar la libreria de los controladores

app = Flask(__name__)

app.secret_key = 'supersecreta'  # Necesaria para manejar los mensajes flash

# Inicializar la base de datos
init_db()  # En lugar de hacer directamente create_all, llamas a tu función


register = FlaskControllerRegister(app)
register.register_package('src.controllers')



# Punto de entrada de la aplicación
if __name__ == '__main__':
    app.run(debug=True)