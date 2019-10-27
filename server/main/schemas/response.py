from marshmallow import Schema, fields

# from main.schemas.category import CategorySchema
# from main.schemas.item import ItemSchema
from main.schemas.user import UserSchema


def create_pagination_response_schema(data_schema, instance=True):
    class PaginationResponseSchema(Schema):
        data = fields.List(fields.Nested(data_schema), required=True)
        per_page = fields.Int(required=True)
        page = fields.Int(required=True)
        total_items = fields.Int(required=True)

    if instance:
        return PaginationResponseSchema()
    return PaginationResponseSchema


# class ItemPaginationResponseSchema(PaginationResponseSchema):
#     data = fields.List(fields.Nested(ItemSchema(many=True)), required=True)
#
#
# class CategoryPaginationResponseSchema(PaginationResponseSchema):
#     data = fields.List(fields.Nested(CategorySchema(many=True)), required=True)


class AuthResponseSchema(Schema):
    access_token = fields.String(required=True)
    user = fields.Nested(UserSchema(only=('id', 'email')), required=True)
