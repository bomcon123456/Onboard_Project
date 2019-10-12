from marshmallow import fields

from ma import ma
from .model import Category
from ..items.schema import ItemSchema


class CategorySchema(ma.Schema):
    id = fields.Integer()
    title = fields.String()
    description = fields.String()
    items = fields.List(fields.Nested(ItemSchema))

    class Meta:
        strict = True
