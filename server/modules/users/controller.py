from flask import Blueprint, request
from flask_jwt import jwt_required, current_identity

from .model import User
from .schema import UserRegisterSchema, UserSchema

user_api = Blueprint('users', __name__)


@user_api.route('', methods=['GET'])
@jwt_required()
def get_authen_user():
    result = UserSchema().dump(current_identity)
    return {
        'message': 'Fetch authen user successfully.',
        'data': result
    }


@user_api.route('', methods=['POST'])
def register():
    data = request.get_json()
    UserRegisterSchema().load(data)

    user = User(**data)
    user.save()

    return {
        'message': 'Create user successfully.',
        'id': user.id
    }
