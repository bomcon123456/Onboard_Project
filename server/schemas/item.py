from marshmallow import Schema, fields, validate


class ItemSchema(Schema):
    id = fields.Integer(required=True, dump_only=True)
    title = fields.String(validate=validate.Length(min=4, max=30), required=True)
    description = fields.String(validate=validate.Length(min=4, max=256), required=True)
    category_id = fields.Integer(required=True)
    creator_id = fields.Integer(required=True)

    class Meta:
        strict = True
