from flask import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity

from main.errors import NotFound, DuplicatedEntity, Forbidden, StatusCodeEnum
from main.models.category import Category
from main.models.item import Item
from main.schemas.item import ItemSchema
from main.schemas.request import ItemPaginationQuerySchema
from main.schemas.response import create_pagination_response_schema
from main.utils.decorators.request_parser import request_parser

item_api = Blueprint('item', __name__)

item_schema = ItemSchema()
items_schema = ItemSchema(many=True)


@item_api.route('/items', methods=['GET'])
@request_parser(query_schema=ItemPaginationQuerySchema())
def gel_all_items(query_params):
    """
    GET all items with pagination
    :param query_params:
    :queryparam page: page that client wants to get, default = 1
    :queryparam per_page: items per page that client wants to get, default = 5
    :queryparam category_id: Identifier or the category to which the items belong

    :raise ValidationError 400: When client passes invalid value for page, per_page
    :return: List of items, current_page, per_page, total.
    """
    query = {}
    # Schema will automatically set category_id to None if client doesn't send a body consisting category_id
    if query_params['category_id'] is not None:
        query['category_id'] = query_params['category_id']

    paginator = Item.query.filter_by(**query) \
        .paginate(page=query_params['page'], per_page=query_params['per_page'], error_out=False)
    raw_response = {
        'data': paginator.items,
        'page': paginator.page,
        'per_page': paginator.per_page,
        'total_items': paginator.total
    }

    return create_pagination_response_schema(data_schema=items_schema).dump(raw_response)


@item_api.route('/items/<int:item_id>', methods=['GET'])
def get_one_item(item_id):
    """
    Get the item with id
    :param item_id: id of the category

    :raise Not Found 404: If item with that id doesn't exist
    :return: Item with that id
    """
    item = Item.find_by_id(item_id)
    if item is None:
        raise NotFound(error_message='Item with this id doesn\'t exist.')

    return {
        'data': item_schema.dump(item)
    }


@item_api.route('/items', methods=['POST'])
@jwt_required
@request_parser(body_schema=ItemSchema(exclude=['creator_id']))
def create_one_item(body_params):
    """
    Create an item
    :param body_params:
    :bodyparam title: Title of the item
    :bodyparam description: Description of the item
    :bodyparam category_id: Identifier of the category to which this item will belong

    :raise ValidationError 400: if form is messed up
    :raise DuplicatedEntity 400: If try to create an existed object.
    :raise BadRequest 400: if the body mimetype is not JSON
    :raise Unauthorized 401: If not login
    :raise NotFound 404: If category_id is not valid
    :return: the created item
    """
    if Category.find_by_id(body_params['category_id']) is None:
        raise NotFound(error_message='Category with this id doesn\'t exist.')
    if Item.query.filter_by(title=body_params['title']).first():
        raise DuplicatedEntity(error_message='Item with this title exists.')

    body_params['creator_id'] = get_jwt_identity()
    item = Item(**body_params)
    item.save()

    return {
        'data': item_schema.dump(item)
    }


@item_api.route('/items/<int:item_id>', methods=['PUT'])
@jwt_required
@request_parser(body_schema=ItemSchema(partial=True))
def update_one_item(item_id, body_params):
    """
    Update the item with id
    :param item_id: ID of the item we want to update
    :param body_params:
    :bodyparam title: Title of the item
    :bodyparam description: Description of the item

    :raise ValidationError 400: if form is messed up
    :raise DuplicatedEntity 400: if there is a item with the title.
    :raise BadRequest 400: if the body mimetype is not JSON
    :raise Unauthorized 401: If not login
    :raise Forbidden 403: If user tries to delete other user's items
    :raise NotFound 404: If category_id is not valid or item with id is not valid
    :return: the updated item
    """
    category_id = body_params.get('category_id')
    # After SchemaValidation, category_id is either None or a number, None will pass through this test
    if category_id and Category.find_by_id(category_id) is None:
        raise NotFound(error_message='Category with this id doesn\'t exist.')

    item = Item.find_by_id(item_id)
    if item is None:
        raise NotFound(error_message='Item with this id doesn\'t exist.')
    if item.creator_id != get_jwt_identity():
        raise Forbidden(error_message='You can\'t update other users\'s item')

    title = body_params.get('title')
    description = body_params.get('description')
    if title:
        if Item.query.filter_by(title=title).first():
            raise DuplicatedEntity(error_message='Item with this title has already existed.')
        item.title = title
    if description:
        item.description = description
    if category_id:
        item.category_id = category_id
    item.save()

    return {
        'data': item_schema.dump(item)
    }


@item_api.route('/items/<int:item_id>', methods=['DELETE'])
@jwt_required
def delete_one_item(item_id):
    """
    Delete the item with id
    :param item_id: ID of the item we want to delete

    :raise Unauthorized 401: If not login
    :raise Forbidden 403: If user tries to delete other user's items
    :raise Not Found 404: If item with that id doesn't exist
    :return: 204 response
    """
    item = Item.find_by_id(item_id)
    if item is None:
        raise NotFound(error_message='Item with this id doesn\'t exist.')
    if item.creator_id != get_jwt_identity():
        raise Forbidden(error_message='You can\'t delete other users\'s item')
    item.delete()

    return {}, StatusCodeEnum.NO_CONTENT
