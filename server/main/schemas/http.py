from marshmallow import Schema, fields, validate


class CategoryPaginationQuerySchema(Schema):
    page = fields.Integer(missing=1, validate=validate.Range(min=1))
    per_page = fields.Int(missing=5, validate=validate.Range(min=1))

    class Meta:
        strict = True


class ItemPaginationQuerySchema(Schema):
    page = fields.Integer(missing=1, validate=validate.Range(min=1))
    per_page = fields.Int(missing=5, validate=validate.Range(min=1))
    category_id = fields.Int(missing=None, validate=validate.Range(min=1))

    class Meta:
        strict = True


class PaginationResponseSchema(Schema):
    data = fields.List(fields.Dict(), required=True)
    per_page = fields.Int(required=True)
    page = fields.Int(required=True)
    total_items = fields.Int(required=True)

    class Meta:
        strict = True
