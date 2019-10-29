from marshmallow import Schema, fields, validate

from main.schemas.custom_fields import TrimmedString


class UserRegisterSchema(Schema):
    email = fields.Email(required=True)
    password = TrimmedString(validate=validate.Length(min=4), required=True)


class UserSchema(Schema):
    id = TrimmedString(required=True, dump_only=True)
    email = fields.Email(required=True)
    created = fields.DateTime(dump_only=True)
    updated = fields.DateTime(dump_only=True)
