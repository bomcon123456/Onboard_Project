from marshmallow import Schema, fields, validate

from main.schemas.category import CategorySchema
from main.schemas.custom_fields import TrimmedString


class ItemSchema(Schema):
    id = fields.Integer(required=True, dump_only=True)
    title = TrimmedString(validate=validate.Length(min=4, max=100), required=True)
    description = TrimmedString(validate=validate.Length(min=4, max=1000), required=True)
    category_id = fields.Integer(required=True, load_only=True)
    category = fields.Nested(CategorySchema(only=('id', 'title')), dump_only=True)
    creator_id = fields.Integer(required=True)
    created = fields.DateTime(dump_only=True)
    updated = fields.DateTime(dump_only=True)
