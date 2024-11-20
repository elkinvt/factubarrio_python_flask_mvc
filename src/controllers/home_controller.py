from src.app import app 
from flask import render_template
from flask_controller import FlaskController

class Home_Controller(FlaskController):
    @app.route('/')
    def index():
        return render_template('index.html')