from marshmallow import Schema, fields, validate

from ..users.schema import UserSchema


class ItemSchema(Schema):
    id = fields.Integer(required=True, dump_only=True)
    title = fields.String(validate=validate.Length(min=4, max=30), required=True)
    description = fields.String(validate=validate.Length(min=4, max=256), required=True)
    category_id = fields.Integer(required=True)
    user_id = fields.Integer(required=True)
    seller = fields.Nested(UserSchema(only=['name']))

    class Meta:
        strict = True
