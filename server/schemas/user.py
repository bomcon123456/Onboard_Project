from marshmallow import Schema, fields, validate


class UserRegisterSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(validate=validate.Length(min=4), required=True)

    class Meta:
        strict = True


class UserSchema(Schema):
    id = fields.Str(required=True, dump_only=True)
    email = fields.Email(required=True)

    class Meta:
        strict = True
