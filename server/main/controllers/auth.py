from flask import Blueprint, request
from flask_jwt_extended import create_access_token
from passlib.hash import bcrypt

from main.models.user import User
from main.schemas.user import UserRegisterSchema
from main.errors import NotFound, FalseAuthentication

auth_api = Blueprint('auth', __name__)


@auth_api.route('', methods=['POST'])
def login():
    """
    POST Authenticate user
    :bodyparam email: email of the user
    :bodyparam password: password of the user

    :raise ValidationError 400: If body of request is messed up
    :raise FalseAuthentication 400: If try to login with a invalid email, password.
    :return: access_token and id of the newly created user
    """
    data = request.get_json()

    email = data.get('email', None)
    password = data.get('password', None)

    UserRegisterSchema().load(data)

    user = User.query.filter_by(email=email).first()
    if not user:
        raise FalseAuthentication('Cant login with the provided information.')
    if bcrypt.verify(password, user.hashed_password):
        access_token = create_access_token(identity=user.id)
        return {'access_token': access_token, 'id': user.id}
    else:
        raise FalseAuthentication('Cant login with the provided information.')
