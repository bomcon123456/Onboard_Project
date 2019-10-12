from marshmallow import fields

from .model import User
from ma import ma


class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'name')


class UserRegisterSchema(ma.Schema):
    username = fields.Str()
    password = fields.Str()
    name = fields.Str()

    class Meta:
        strict = True
