from marshmallow import Schema, fields, validate


class BasePaginationQuerySchema(Schema):
    page = fields.Integer(missing=1, validate=validate.Range(min=1))
    per_page = fields.Int(missing=5, validate=validate.Range(min=1))


class ItemPaginationQuerySchema(BasePaginationQuerySchema):
    category_id = fields.Int(missing=None, validate=validate.Range(min=1))
