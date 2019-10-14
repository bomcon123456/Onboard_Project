from flask import Blueprint, request, abort
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token

from models.user import User
from schemas.user import UserRegisterSchema, UserSchema
from utils.customexceptions import NotFound, DuplicatedEntity

user_api = Blueprint('users', __name__)


@user_api.route('/<int:_id>', methods=['GET'])
@jwt_required
def get_user(_id):
    """
    GET authenticated user
    :requires: Login-ed user

    :raise Unauthorized 401: If user is not login-ed
    :raise NotFound 404: If user doesn't exist.
    :return: Information of login-ed user
    """
    user_id = get_jwt_identity()
    if user_id != _id:
        abort(403)

    user = User.find_by_id(_id)
    if not user:
        raise NotFound('Can\'t find user with this id.')

    result = UserSchema().dump(user)
    return {
        'data': result
    }


@user_api.route('', methods=['POST'])
def register():
    """
    Create new user

    :bodyparam email: email of the user
    :bodyparam password: password of the user

    :raise ValidationError 400: If body of request is messed up
    :raise DuplicatedEntity 400: If try to create an existed object.
    :raise IntegrityError1062 400: If try to create an existed user
    :return: access_token and id of the newly created user
    """
    data = request.get_json()
    UserRegisterSchema().load(data)

    if User.query.filter_by(email=data['email']).first():
        raise DuplicatedEntity()

    user = User(**data)
    user.save()

    access_token = create_access_token(identity=user.id)

    return {
        'access_token': access_token,
        'id': user.id
    }
