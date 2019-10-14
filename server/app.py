import os

from dotenv import load_dotenv
from flask import Flask
from flask_jwt import JWT

from errorhandlers import error_handlers
from controllers.category import category_api
from controllers.item import item_api
from controllers.user import user_api
from security import authenticate, identity

app = Flask(__name__)
load_dotenv()

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['JWT_AUTH_URL_RULE'] = '/api/v1/auth'
app.secret_key = os.environ.get('APP_SECRET_KEY')

app.register_blueprint(error_handlers)

app.register_blueprint(user_api, url_prefix='/api/v1/users')
app.register_blueprint(category_api, url_prefix='/api/v1/categories')
app.register_blueprint(item_api, url_prefix='/api/v1/items')

jwt = JWT(app, authenticate, identity)
