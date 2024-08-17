from flask import Flask, render_template


app = Flask(__name__, template_folder='docs')

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

@app.route('/cerrar_sesion')
def cerrar_sesion():
    return render_template('index.html')