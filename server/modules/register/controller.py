from flask import Blueprint, request

from ..users.model import User
from ..users.schema import UserSchema, UserRegisterSchema

register_api = Blueprint('register', __name__)

user_schema = UserSchema()


@register_api.route('', methods=['POST'])
def register():
    data = request.get_json()
    UserRegisterSchema().load(data)

    user = User(**data)
    user.save()

    return {
        'message': 'Registration completed.',
        'id': user.id
    }
