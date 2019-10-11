from flask import Blueprint, request
from marshmallow import ValidationError, fields
from ma import ma

from ..users.model import User
from ..users.schema import UserSchema

register_api = Blueprint('register',__name__)

class UserRegisterSchema(ma.Schema):
    username = fields.Str()
    password = fields.Str()
    name = fields.Str()
    class Meta:
        strict = True


@register_api.route('', methods=['POST'])
def register():
    data = request.get_json()
    try:
        result = UserRegisterSchema().load(data)
        print(result)
        user = User(**result)
        user.save()
        user_schema = UserSchema()
        return user_schema.jsonify(user)
    except ValidationError as e:
        # TODO Handle ValidationError
        print(e.messages)


