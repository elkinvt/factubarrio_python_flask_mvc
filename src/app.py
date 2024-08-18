from flask import Flask, render_template


app = Flask(__name__)

if __name__ == '__main__':
    app.run(debug = True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/pagina_pricipal')
def pagina_principal():
    return render_template('pgprincipal.html')

@app.route('/clientes_crear')
def clientes_crear():
    return render_template('form_crear_cliente.html')

@app.route('/clientes_ver')
def clientes_ver():
    return render_template('form_ver_cliente.html')

@app.route('/clientes_editar')
def clientes_editar():
    return render_template('form_editar_cliente.html')

@app.route('/vendedores_crear')
def vendedores_crear():
    return render_template('form_crear_vendedor.html')

@app.route('/vendedores_ver')
def vendedores_ver():
    return render_template('form_ver_vendedor.html')

@app.route('/vendedores_editar')
def vendedores_editar():
    return render_template('form_editar_vendedor.html')

@app.route('/productos_crear')
def productos_crear():
    return render_template('form_crear_producto.html')

@app.route('/productos_ver')
def productos_ver():
    return render_template('form_ver_producto.html')

@app.route('/productos_editar')
def productos_editar():
    return render_template('form_editar_producto.html')

@app.route('/usuarios_crear')
def usuarios_crear():
    return render_template('form_crear_usuario.html')

@app.route('/usuarios_ver')
def usuarios_ver():
    return render_template('form_ver_usuario.html')

@app.route('/usuarios_editar')
def usuarios_editar():
    return render_template('form_editar_usuario.html')

@app.route('/generar_factura')
def generar_factura():
    return render_template('form_generacion_factura.html')

@app.route('/ver_factura')
def ver_factura():
    return render_template('form_ver_factura.html')

@app.route('/cerrar_sesion')
def cerrar_sesion():
    return render_template('index.html')