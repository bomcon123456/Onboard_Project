from marshmallow import Schema, fields, validate


class UserRegisterSchema(Schema):
    username = fields.Str(validate=validate.Length(min=4))
    password = fields.Str(validate=validate.Length(min=4))
    name = fields.Str(validate=validate.Length(min=4))

    class Meta:
        strict = True


class UserSchema(Schema):
    username = fields.Str(validate=validate.Length(min=4))
    name = fields.Str(validate=validate.Length(min=4))

    class Meta:
        strict = True
