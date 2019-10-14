from flask import Blueprint, request
from flask_jwt_extended import create_access_token

from passlib.hash import bcrypt

from models.user import User
from schemas.user import UserRegisterSchema
from utils.customexceptions import NotFound, FalseAuthentication

auth_api = Blueprint('auth', __name__)


@auth_api.route('', methods=['POST'])
def login():
    data = request.get_json()

    username = data.get('username', None)
    password = data.get('password', None)

    UserRegisterSchema().load(data)

    user = User.query.filter_by(username=username).first()
    if not user:
        raise NotFound('Can\'t find user with that username.')
    if bcrypt.verify(password, user.hashed_password):
        access_token = create_access_token(identity=user.id)
        return {'access_token': access_token, 'id': user.id}
    else:
        raise FalseAuthentication('Please enter valid password.')
