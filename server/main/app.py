from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from main.controllers.auth import auth_api
from main.controllers.category import category_api
from main.controllers.item import item_api
from main.controllers.user import user_api
from main.errors import error_handlers
from main.utils.config_helpers import choose_config


def create_app(app_type):
    app = Flask(__name__)

    app.config.from_object(choose_config(app_type))

    JWTManager(app)
    CORS(app)

    app.register_blueprint(error_handlers)

    app.register_blueprint(user_api)
    app.register_blueprint(category_api)
    app.register_blueprint(item_api)
    app.register_blueprint(auth_api)

    return app
