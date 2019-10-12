from flask import Blueprint, request, abort
from flask_jwt import jwt_required, current_identity

from common.customexceptions import NotFound
from .model import Item
from .schema import ItemSchema

item_api = Blueprint('item', __name__)

item_schema = ItemSchema()
categories_schema = ItemSchema(many=True)


@item_api.route('', methods=['GET'])
def get():
    """
    GET method for Item

    :queryparam page: page that client wants to get, default = 1
    :queryparam size: item per page that client wants to get, default = 5

    :return: List of categories, currentPage, perPage, total.
    """
    page = request.args.get('page', 1)
    size = request.args.get('size', 5)

    paginator = Item.query.paginate(page, size, False)
    result = categories_schema.dump(paginator.items)

    return {
        'message': 'Fetch categories successfully.',
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

    :raise: Not found
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
    :return: id of the newly created item
    """
    body = request.get_json()
    body['user_id'] = current_identity.id

    item_schema.load(body)

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
    :return: id of the newly created item
    """
    body = request.get_json()

    item_schema.load(body)

    item = Item.find_by_id(_id)
    if item is None:
        body['user_id'] = current_identity.id
        item = Item(**body)
    else:
        if item.user_id != current_identity.id:
            abort(403)
        item.title = body.get('title', item.title)
        item.description = body.get('description', item.description)

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

    :return: 204 response
    """
    item = Item.find_by_id(_id)
    if item is None:
        return {
                   'message': 'This item doesn\'t exist.',
               }, 404
    else:
        if item.user_id != current_identity.id:
            abort(403)
        item.delete()

    return {
               'message': 'Delete item successfully.',
           }, 204
