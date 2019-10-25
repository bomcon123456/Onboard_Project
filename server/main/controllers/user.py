from flask import Blueprint, request
from flask_jwt_extended import create_access_token

from main.errors import DuplicatedEntity
from main.models.user import User
from main.schemas.http import AuthResponseSchema
from main.schemas.user import UserRegisterSchema

user_api = Blueprint('users', __name__)


@user_api.route('/users', methods=['POST'])
def register():
    """
    Create new user

    :bodyparam email: email of the user
    :bodyparam password: password of the user

    :raise ValidationError 400: If body of request is messed up
    :raise DuplicatedEntity 400: If try to create an existed object.
    :return: access_token and id of the newly created user
    """
    data = request.get_json()

    UserRegisterSchema().load(data)

    email = data.get('email', None)
    if email and User.query.filter_by(email=email).first():
        raise DuplicatedEntity(error_message='User with this email exists.')

    user = User(**data)
    user.save()

    access_token = create_access_token(identity=user.id)
    raw_data = {
        'access_token': access_token,
        'user': user
    }
    return AuthResponseSchema().dump(raw_data)
