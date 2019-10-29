from marshmallow import Schema, fields

from main.schemas.user import UserSchema


def create_pagination_response_schema(data_schema, instance=True):
    class PaginationResponseSchema(Schema):
        data = fields.List(fields.Nested(data_schema), required=True, attribute='items')
        per_page = fields.Integer(required=True, attribute='per_page')
        page = fields.Integer(required=True, attribute='page')
        total_items = fields.Integer(required=True, attribute='total')

    if instance:
        return PaginationResponseSchema()
    return PaginationResponseSchema


class AuthResponseSchema(Schema):
    access_token = fields.String(required=True)
    user = fields.Nested(UserSchema(only=('id', 'email')), required=True)
