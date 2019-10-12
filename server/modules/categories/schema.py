from marshmallow import Schema, fields, validate

from ..items.schema import ItemSchema


class CategorySchema(Schema):
    id = fields.Integer()
    title = fields.String(validate=validate.Length(min=4, max=30))
    description = fields.String(validate=validate.Length(min=4, max=256))
    items = fields.List(fields.Nested(ItemSchema))

    class Meta:
        strict = True
