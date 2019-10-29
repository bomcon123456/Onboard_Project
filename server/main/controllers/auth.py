from flask import Blueprint
from flask_jwt_extended import create_access_token
from passlib.hash import bcrypt

from main.errors import FalseAuthentication
from main.models.user import UserModel
from main.schemas.response import AuthResponseSchema
from main.schemas.user import UserRegisterSchema
from main.utils.decorators.request_parser import request_parser

auth_api = Blueprint('auth', __name__)


@auth_api.route('/auth', methods=['POST'])
@request_parser(body_schema=UserRegisterSchema())
def login(body_params):
    """
    POST Authenticate user
    :param body_params:
    :bodyparam email: email of the user
    :bodyparam password: password of the user

    :raise ValidationError 400: If body of request is messed up
    :raise BadRequest 400: if the body mimetype is not JSON
    :return: access_token and {id, email} of the newly created user
    """
    email = body_params.get('email')
    password = body_params.get('password')

    user = UserModel.query.filter_by(email=email).first()
    if user is None or not bcrypt.verify(password, user.hashed_password):
        raise FalseAuthentication('Cant login with the provided information.')

    access_token = create_access_token(identity=user.id)
    raw_data = {'access_token': access_token, 'user': user}

    return AuthResponseSchema().dump(raw_data)
