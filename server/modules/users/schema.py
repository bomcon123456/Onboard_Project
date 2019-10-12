from marshmallow import Schema, fields, validate


class UserRegisterSchema(Schema):
    username = fields.Str(validate=validate.Length(min=4), required=True)
    password = fields.Str(validate=validate.Length(min=4), required=True)
    name = fields.Str(validate=validate.Length(min=4), required=True)

    class Meta:
        strict = True


class UserSchema(Schema):
    id = fields.Str(required=True, dump_only=True)
    username = fields.Str(validate=validate.Length(min=4), required=True)
    name = fields.Str(validate=validate.Length(min=4), required=True)

    class Meta:
        strict = True
