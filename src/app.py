from flask import Flask, render_template


app = Flask(__name__)

if __name__ == '__main__':
    app.run(debug = True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/pagina_principal')
def pagina_principal():
    return render_template('pgprincipal.html', titulo_pagina ="Pagina principal")

@app.route('/clientes_crear')
def clientes_crear():
    return render_template('form_crear_cliente.html', titulo_pagina = "Crear cliente")

@app.route('/clientes_ver')
def clientes_ver():
    return render_template('form_ver_cliente.html', titulo_pagina = "Ver cliente")

@app.route('/clientes_editar')
def clientes_editar():
    return render_template('form_editar_cliente.html', titulo_pagina = "Editar cliente")

@app.route('/vendedores_crear')
def vendedores_crear():
    return render_template('form_crear_vendedor.html', titulo_pagina = "Crear vendedor")

@app.route('/vendedores_ver')
def vendedores_ver():
    return render_template('form_ver_vendedor.html', titulo_pagina = "Ver vendedor")

@app.route('/vendedores_editar')
def vendedores_editar():
    return render_template('form_editar_vendedor.html', titulo_pagina = "Editar vendedor")

@app.route('/productos_crear')
def productos_crear():
    return render_template('form_crear_producto.html', titulo_pagina = " Crear producto")

@app.route('/productos_ver')
def productos_ver():
    return render_template('form_ver_producto.html', titulo_pagina = "Ver producto")

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