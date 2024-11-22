from src.app import app 
from flask import render_template
from flask_controller import FlaskController

class Login_Controller(FlaskController):
    @app.route('/')
    def Login():
        return render_template('login.html')