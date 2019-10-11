import os

from flask import Flask
from dotenv import load_dotenv
from flask_jwt import JWT

from modules.register.controller import register_api
from security import authenticate, identity

app = Flask(__name__)
load_dotenv()

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.secret_key = os.environ.get('APP_SECRET_KEY')

app.register_blueprint(register_api, url_prefix='/register')

jwt = JWT(app, authenticate, identity)
