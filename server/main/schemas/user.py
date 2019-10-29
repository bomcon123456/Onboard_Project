from marshmallow import Schema, fields, validate


class UserRegisterSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(validate=validate.Length(min=4), required=True)


class UserSchema(Schema):
    id = fields.String(required=True, dump_only=True)
    email = fields.Email(required=True)
    created = fields.DateTime(dump_only=True)
    updated = fields.DateTime(dump_only=True)
