from flask import Flask, render_template


from models import Base, engine  # Importar la base y el engine para crear las tablas
from models import init_db  # Importar la función init_db para crear las tablas

# Importa las rutas con nombres únicos
from rutas.clientes_rutas import registrar_rutas as registrar_rutas_clientes
from rutas.vendedores_rutas import registrar_rutas as registrar_rutas_vendedores
from rutas.productos_rutas import registrar_rutas as registrar_rutas_productos

app = Flask(__name__)

app.secret_key = 'supersecreta'  # Necesaria para manejar los mensajes flash



# Inicializar la base de datos
init_db()  # En lugar de hacer directamente create_all, llamas a tu función



# Registra las rutas
registrar_rutas_clientes(app)
registrar_rutas_vendedores(app)
registrar_rutas_productos(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/pagina_principal')
def pagina_principal():
    return render_template('pgprincipal.html', titulo_pagina ="Pagina principal")




@app.route('/productos_editar')
def productos_editar():
    return render_template('form_editar_producto.html', titulo_pagina = "Editar producto")

@app.route('/usuarios_crear')
def usuarios_crear():
    return render_template('form_crear_usuario.html', titulo_pagina = "Crear usuario")

@app.route('/usuarios_ver')
def usuarios_ver():
    return render_template('form_ver_usuario.html', titulo_pagina = "Ver usuario")

@app.route('/usuarios_editar')
def usuarios_editar():
    return render_template('form_editar_usuario.html', titulo_pagina = "Editar usuario")

@app.route('/generar_factura')
def generar_factura():
    return render_template('form_generacion_factura.html', titulo_pagina = "Generar factura")

@app.route('/ver_factura')
def ver_factura():
    return render_template('form_ver_factura.html', titulo_pagina = "Ver factura")

@app.route('/cerrar_sesion')
def cerrar_sesion():
    return render_template('index.html')

# Punto de entrada de la aplicación
if __name__ == '__main__':
    app.run(debug=True)