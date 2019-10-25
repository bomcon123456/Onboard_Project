from flask import Blueprint
from flask_jwt_extended import create_access_token

from main.errors import DuplicatedEntity
from main.models.user import User
from main.schemas.response import AuthResponseSchema
from main.schemas.user import UserRegisterSchema
from main.utils.decorators.request_parser import request_parser

user_api = Blueprint('users', __name__)


@user_api.route('/users', methods=['POST'])
@request_parser(body_schema=UserRegisterSchema())
def register(body_params):
    """
    Create new user

    :param body_params:
    :bodyparams: email: email of the user
    :bodyparams: password: password of the user

    :raise ValidationError 400: If body of request is messed up
    :raise DuplicatedEntity 400: If try to create an existed object.
    :return: access_token and id of the newly created user
    """
    email = body_params.get('email')
    if email and User.query.filter_by(email=email).first():
        raise DuplicatedEntity(error_message='User with this email exists.')

    user = User(**body_params)
    user.save()

    access_token = create_access_token(identity=user.id)
    raw_data = {
        'access_token': access_token,
        'user': user
    }

    return AuthResponseSchema().dump(raw_data)
