from marshmallow import Schema, fields, validate

from ..items.schema import ItemSchema


class CategorySchema(Schema):
    id = fields.Integer(required=True)
    title = fields.String(validate=validate.Length(min=4, max=30), required=True)
    description = fields.String(validate=validate.Length(min=4, max=256), required=True)
    items = fields.List(fields.Nested(ItemSchema), required=True)

    class Meta:
        strict = True
