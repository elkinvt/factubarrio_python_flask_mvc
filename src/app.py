from flask import Flask
from src.models import Base, engine  # Importar la base y el engine para crear las tablas
from flask_controller import FlaskControllerRegister #importar la libreria de los controladores
from flask_login import LoginManager
from src.models.usuarios import Usuarios
from src.models import  Base, SessionLocal 

app = Flask(__name__)

app.secret_key = 'supersecreta'  # Necesaria para manejar los mensajes flash

register = FlaskControllerRegister(app)
register.register_package('src.controllers')

# Crear todas las tablas
Base.metadata.create_all(bind=engine)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(id_usuario):
    session = SessionLocal()
    try:
        return session.query(Usuarios).get(int(id_usuario))
    finally:
        session.close()


# Punto de entrada de la aplicación
if __name__ == '__main__':
    app.run(debug=True)