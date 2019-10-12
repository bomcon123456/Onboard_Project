import os

from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_jwt import JWT
from marshmallow import ValidationError
from sqlalchemy import exc

from modules.register.controller import register_api
from modules.categories.controller import category_api
from modules.items.controller import item_api

from security import authenticate, identity

app = Flask(__name__)
load_dotenv()

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.secret_key = os.environ.get('APP_SECRET_KEY')


@app.errorhandler(ValidationError)
def handle_invalid_form(error):
    response = jsonify({
        'message': '[ERROR]: Bad request form.', 'errors': error.messages
    })
    response.status_code = 400
    return response


@app.errorhandler(exc.IntegrityError)
def handle_database_error(error):
    error_info = error.orig.args
    response = jsonify({
        'message': '[ERROR]: Try to create a new entity that has already existed.',
        'errors': error_info[1]
    })
    if (error_info[0] == 1062):
        response.status_code = 400
    else:
        response.status_code = 500
    return response


@app.errorhandler(Exception)
def handle_all_errors(error):
    response = jsonify({
        'message': '[ERROR]: Internal Server Error.'
    })
    response.status_code = 500
    return response


app.register_blueprint(register_api, url_prefix='/register')
app.register_blueprint(category_api, url_prefix='/categories')
app.register_blueprint(item_api, url_prefix='/items')

jwt = JWT(app, authenticate, identity)
