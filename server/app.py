import os

from dotenv import load_dotenv
from flask import Flask
from flask_jwt import JWT

from modules.register.controller import register_api
from modules.categories.controller import category_api
from modules.items.controller import item_api
from errorhandlers import error_handlers

from security import authenticate, identity

app = Flask(__name__)
load_dotenv()

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.secret_key = os.environ.get('APP_SECRET_KEY')

app.register_blueprint(error_handlers)

app.register_blueprint(register_api, url_prefix='/register')
app.register_blueprint(category_api, url_prefix='/categories')
app.register_blueprint(item_api, url_prefix='/items')

jwt = JWT(app, authenticate, identity)
