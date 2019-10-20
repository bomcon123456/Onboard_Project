import os

from dotenv import load_dotenv
from flask import Flask
from flask_jwt_extended import JWTManager

from main.errors import error_handlers
from main.controllers.category import category_api
from main.controllers.item import item_api
from main.controllers.user import user_api
from main.controllers.auth import auth_api

app = Flask(__name__)
load_dotenv()

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')
app.config['JWT_ERROR_MESSAGE_KEY'] = 'message'
app.secret_key = os.environ.get('APP_SECRET_KEY')

jwt = JWTManager(app)

app.register_blueprint(error_handlers)

app.register_blueprint(user_api, url_prefix='/users')
app.register_blueprint(category_api, url_prefix='/categories')
app.register_blueprint(item_api, url_prefix='/items')
app.register_blueprint(auth_api, url_prefix='/auth')
