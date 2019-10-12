from marshmallow import Schema, fields, validate

from ..items.schema import ItemSchema


class CategorySchema(Schema):
    id = fields.Integer(required=True, dump_only=True)
    title = fields.String(validate=validate.Length(min=4, max=30), required=True)
    description = fields.String(validate=validate.Length(min=4, max=256), required=True)
    items = fields.Nested(ItemSchema(only=['author', 'id', 'title', 'description']), required=True, many=True,
                          dump_only=True)

    class Meta:
        strict = True
