from flask import Flask, render_template


app = Flask(__name__, template_folder='docs')

if __name__ == '__main__':
    app.run(debug = True)

@app.route('/')

def index():
    return render_template('index.html')