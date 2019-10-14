from marshmallow import Schema, fields, validate


class CategorySchema(Schema):
    id = fields.Integer(required=True, dump_only=True)
    title = fields.String(validate=validate.Length(min=4, max=30), required=True)
    description = fields.String(validate=validate.Length(min=4, max=256), required=True)
    creator_id = fields.Int(required=True)

    class Meta:
        strict = True
