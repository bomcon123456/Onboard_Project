from marshmallow import Schema, fields, validate

from main.schemas.category import CategorySchema


class ItemSchema(Schema):
    id = fields.Integer(required=True, dump_only=True)
    title = fields.String(validate=validate.Length(min=4, max=30), required=True)
    description = fields.String(validate=validate.Length(min=4, max=256), required=True)
    category_id = fields.Integer(required=True, load_only=True)
    category = fields.Nested(CategorySchema(only=('id', 'title')))
    creator_id = fields.Integer(required=True)
    created = fields.DateTime(dump_only=True)
    updated = fields.DateTime(dump_only=True)

    class Meta:
        strict = True
