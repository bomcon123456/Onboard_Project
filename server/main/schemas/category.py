from marshmallow import Schema, fields, validate


class CategorySchema(Schema):
    id = fields.Integer(required=True, dump_only=True)
    title = fields.String(validate=validate.Length(min=4, max=100), required=True)
    description = fields.String(validate=validate.Length(min=4, max=1000), required=True)
    creator_id = fields.Int(required=True)
    created = fields.DateTime(dump_only=True)
    updated = fields.DateTime(dump_only=True)

    class Meta:
        strict = True
