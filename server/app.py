import os

from dotenv import load_dotenv
from flask import Flask
from flask_jwt import JWT

from errorhandlers import error_handlers
from modules.categories.controller import category_api
from modules.items.controller import item_api
from modules.users.controller import user_api
from security import authenticate, identity

app = Flask(__name__)
load_dotenv()

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.secret_key = os.environ.get('APP_SECRET_KEY')

app.register_blueprint(error_handlers)

app.register_blueprint(user_api, url_prefix='/users')
app.register_blueprint(category_api, url_prefix='/categories')
app.register_blueprint(item_api, url_prefix='/items')

jwt = JWT(app, authenticate, identity)
