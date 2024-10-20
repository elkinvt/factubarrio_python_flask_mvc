from flask import Flask, render_template


from src.models import Base, engine  # Importar la base y el engine para crear las tablas
from src.models import init_db  # Importar la función init_db para crear las tablas

#importar la libreria de los controladores
from flask_controller import FlaskControllerRegister



app = Flask(__name__)

app.secret_key = 'supersecreta'  # Necesaria para manejar los mensajes flash



# Inicializar la base de datos
init_db()  # En lugar de hacer directamente create_all, llamas a tu función


register = FlaskControllerRegister(app)
register.register_package('src.controllers')



@app.route('/usuarios_crear')
def usuarios_crear():
    return render_template('form_crear_usuario.html', titulo_pagina = "Crear usuario")

@app.route('/usuarios_ver')
def usuarios_ver():
    return render_template('form_ver_usuario.html', titulo_pagina = "Ver usuario")

@app.route('/usuarios_editar')
def usuarios_editar():
    return render_template('form_editar_usuario.html', titulo_pagina = "Editar usuario")






# Punto de entrada de la aplicación
if __name__ == '__main__':
    app.run(debug=True)