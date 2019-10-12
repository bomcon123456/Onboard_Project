from flask import Blueprint, request
from flask_jwt import jwt_required, current_identity

from .model import User
from .schema import UserRegisterSchema, UserSchema

user_api = Blueprint('users', __name__)


@user_api.route('', methods=['GET'])
@jwt_required()
def get_authen_user():
    """
    GET authenticated user
    :requires: Login-ed user

    :raise Unauthorized 401: If user is not login-ed
    :return: Information of login-ed user
    """
    result = UserSchema().dump(current_identity)
    return {
        'message': 'Fetch authen user successfully.',
        'data': result
    }


@user_api.route('', methods=['POST'])
def register():
    """
    Create new user

    :bodyparam username: username of the user
    :bodyparam password: password of the user
    :bodyparam name: name of the user

    :raise ValidationError 400: If body of request is messed up
    :raise IntegrityError1062 400: If try to create an existed user
    :return: id of the newly created user
    """
    data = request.get_json()
    UserRegisterSchema().load(data)

    user = User(**data)
    user.save()

    return {
        'message': 'Create user successfully.',
        'id': user.id
    }
