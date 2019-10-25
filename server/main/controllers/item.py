from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from main.errors import NotFound, DuplicatedEntity, Forbidden, StatusCodeEnum
from main.models.category import Category
from main.models.item import Item
from main.schemas.http import ItemPaginationQuerySchema, PaginationResponseSchema
from main.schemas.item import ItemSchema
from main.utils.decorators import request_parser

item_api = Blueprint('item', __name__)

item_schema = ItemSchema()
items_schema = ItemSchema(many=True)


@item_api.route('/items', methods=['GET'])
@request_parser(ItemPaginationQuerySchema)
def get(query_params):
    """
    GET method for Item

    :queryparam page: page that client wants to get, default = 1
    :queryparam per_page: item per page that client wants to get, default = 5
    :queryparam category_id: category to which the client wants to get the items belong

    :raise ValidationError 400: When client passes invalid value for page, per_page
    :return: List of items, current_page, per_page, total.
    """

    query = {}
    if query_params['category_id'] is not None:
        query['category_id'] = query_params['category_id']

    paginator = Item.query.filter_by(**query) \
        .paginate(page=query_params['page'], per_page=query_params['per_page'], error_out=False)
    result = items_schema.dump(paginator.items)

    raw_response = {
        'data': result,
        'page': paginator.page,
        'per_page': paginator.per_page,
        'total_items': paginator.total
    }
    return PaginationResponseSchema().dump(raw_response)


@item_api.route('/items/<int:item_id>', methods=['GET'])
def get_one(item_id):
    """
    GET one method for Category
    :param item_id: id of the category

    :raise Not Found 404: If item with that id doesn't exist
    :return: Item with that id
    """
    item = Item.find_by_id(item_id)
    if item is None:
        raise NotFound(error_message='Item with this id doesn\'t exist.')
    else:
        return {
            'data': item_schema.dump(item)
        }


@item_api.route('/items', methods=['POST'])
@jwt_required
def post():
    """
    POST method for Item
    :requires: must be login-ed

    :bodyparam title: Title of the item
    :bodyparam description: Description of the item
    :bodypram category_id: Category of the item

    :raise: ValidationError 400: if form is messed up
    :raise DuplicatedEntity 400: If try to create an existed object.
    :raise Unauthorized 401: If not login
    :raise NotFound 404: If category_id is not valid
    :return: the created item
    """

    body = request.get_json()
    body['creator_id'] = get_jwt_identity()

    item_schema.load(body)

    if Category.find_by_id(body['category_id']) is None:
        raise NotFound(error_message='Category with this id doesn\'t exist.')

    if Item.query.filter_by(title=body['title']).first():
        raise DuplicatedEntity(error_message='Item with this title exists.')

    item = Item(**body)
    item.save()

    return {
        'data': item_schema.dump(item)
    }


@item_api.route('/items/<int:item_id>', methods=['PUT'])
@jwt_required
def put(item_id):
    """
    PUT method for Item
    :requires: the login-ed user must be the one created this item

    :param item_id: ID of the item we want to update

    :bodyparam title: Title of the item
    :bodyparam description: Description of the item

    :raise ValidationError 400: if form is messed up
    :raise DuplicatedEntity 400: if there is a item with the title.
    :raise Unauthorized 401: If not login
    :raise Forbidden 403: If user tries to delete other user's items
    :raise NotFound 404: If category_id is not valid or item with id is not valid
    :return: the updated item
    """
    body = request.get_json()
    body['creator_id'] = get_jwt_identity()

    category_id = body.get('category_id', None)
    if category_id and Category.find_by_id(category_id) is None:
        raise NotFound(error_message='Category with this id doesn\'t exist.')

    item = Item.find_by_id(item_id)
    if item is None:
        raise NotFound(error_message='Item with this id doesn\'t exist.')
    else:
        ItemSchema(partial=True).load(body)

        title = body.get('title', None)
        if title and Item.query.filter_by(title=title).first():
            raise DuplicatedEntity(error_message='Item with this title has already existed.')

        if item.creator_id != get_jwt_identity():
            raise Forbidden('You can\'t update other users\'s item')
        item.title = title or item.title
        item.description = body.get('description', item.description)
        item.category_id = category_id or item.category_id

    item.save()

    return {
        'data': item_schema.dump(item)
    }


@item_api.route('/items/<int:item_id>', methods=['DELETE'])
@jwt_required
def delete(item_id):
    """
    DELETE method for Item
    :param item_id: ID of the item we want to delete

    :raise Unauthorized 401: If not login
    :raise Forbidden 403: If user tries to delete other user's items
    :raise Not Found 404: If item with that id doesn't exist
    :return: 204 response
    """
    item = Item.find_by_id(item_id)
    if item is None:
        raise NotFound(error_message='Item with this id doesn\'t exist.')
    else:
        if item.creator_id != get_jwt_identity():
            raise Forbidden('You can\'t delete other users\'s item')
        item.delete()

    return {}, StatusCodeEnum.NO_CONTENT
