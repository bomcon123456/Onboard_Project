from flask import Blueprint, request, abort
from flask_jwt import jwt_required, current_identity

from common.customexceptions import NotFound
from models.item import Item
from schemas.item import ItemSchema
from models.category import Category

item_api = Blueprint('item', __name__)

item_schema = ItemSchema()
categories_schema = ItemSchema(many=True)


@item_api.route('', methods=['GET'])
def get():
    """
    GET method for Item

    :queryparam page: page that client wants to get, default = 1
    :queryparam size: item per page that client wants to get, default = 5
    :queryparam category_id: items of which category having id = category_id

    :return: List of items, currentPage, perPage, total.
    """
    page = request.args.get('page', 1)
    size = request.args.get('size', 5)
    category_id = request.args.get('category_id', None)
    query = {}
    if category_id is not None:
        query['category_id'] = category_id

    paginator = Item.query.filter_by(**query).paginate(page, size, False)
    result = categories_schema.dump(paginator.items)

    return {
        'message': 'Fetch items successfully.',
        'data': result,
        'currentPage': paginator.page,
        'perPage': paginator.per_page,
        'total': paginator.total
    }


@item_api.route('<int:_id>', methods=['GET'])
def get_one(_id):
    """
    GET one method for Category
    :param _id: id of the category

    :raise Not Found 404: If item with that id doesn't exist
    :return: Item with that id
    """
    item = Item.find_by_id(_id)
    if item is None:
        raise NotFound(message='Item with this id doesn\'t exists.')
    else:
        return {
            'message': 'Fetch item successfully.',
            'data': item_schema.dump(item)
        }


@item_api.route('', methods=['POST'])
@jwt_required()
def post():
    """
    POST method for Item
    :requires: must be login-ed

    :bodyparam title: Title of the item
    :bodyparam description: Description of the item
    :bodypram category_id: Category of the item

    :raise: ValidationError if form is messed up
    :raise Unauthorized 401: If not login
    :raise Forbidden 403: If user tries to delete other user's items
    :raise NotFound 404: If category_id is not valid
    :return: id of the newly created item
    """
    body = request.get_json()
    body['user_id'] = current_identity.id

    item_schema.load(body)

    if Category.find_by_id(body['category_id']) is None:
        raise NotFound('Category with this id doesn\'t exist.')

    item = Item(**body)
    item.save()

    return {
        'message': 'Create item successfully.',
        'id': item.id
    }


@item_api.route('/<int:_id>', methods=['PUT'])
@jwt_required()
def put(_id):
    """
    PUT method for Item
    :requires: the login-ed user must be the one created this item

    :param _id: ID of the item we want to update

    :bodyparam title: Title of the item
    :bodyparam description: Description of the item

    :raise: ValidationError if form is messed up
    :raise Unauthorized 401: If not login
    :raise Forbidden 403: If user tries to delete other user's items
    :raise NotFound 404: If category_id is not valid
    :return: id of the newly created item
    """
    body = request.get_json()
    body['user_id'] = current_identity.id
    category_id = body.get('category_id', None)
    if category_id and Category.find_by_id(category_id) is None:
        raise NotFound('Category with this id doesn\'t exist.')

    item = Item.find_by_id(_id)
    if item is None:
        item_schema.load(body)

        item = Item(**body)
    else:
        ItemSchema(partial=True).load(body)

        if item.user_id != current_identity.id:
            abort(403)
        item.title = body.get('title', item.title)
        item.description = body.get('description', item.description)
        item.category_id = category_id or item.category_id

    item.save()

    return {
        'message': 'Update item successfully.',
        'id': item.id
    }


@item_api.route('/<int:_id>', methods=['DELETE'])
@jwt_required()
def delete(_id):
    """
    DELETE method for Item
    :param _id: ID of the item we want to delete

    :raise Not Found 404: If item with that id doesn't exist
    :raise Unauthorized 401: If not login
    :raise Forbidden 403: If user tries to delete other user's items
    :return: 204 response
    """
    item = Item.find_by_id(_id)
    if item is None:
        raise NotFound(message='Item with this id doesn\'t exists.')
    else:
        if item.user_id != current_identity.id:
            abort(403)
        item.delete()

    return {
               'message': 'Delete item successfully.',
           }, 204
