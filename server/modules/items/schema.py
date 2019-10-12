from marshmallow import Schema, fields, validate


class ItemSchema(Schema):
    id = fields.Integer()
    title = fields.String(validate=validate.Length(min=4, max=30))
    description = fields.String(validate=validate.Length(min=4, max=256))
    category_id = fields.Integer()
    user_id = fields.Integer()

    class Meta:
        strict = True
