from flask import Blueprint, request, abort
from flask_jwt_extended import jwt_required, get_jwt_identity

from main.utils.customexceptions import NotFound, DuplicatedEntity
from main.models.item import Item
from main.schemas.item import ItemSchema
from main.models.category import Category

item_api = Blueprint('item', __name__)

item_schema = ItemSchema()
categories_schema = ItemSchema(many=True)


@item_api.route('', methods=['GET'])
def get():
    """
    GET method for Item

    :queryparam page: page that client wants to get, default = 1
    :queryparam size: item per page that client wants to get, default = 5

    :return: List of items, current_page, per_page, total.
    """
    page = request.args.get('page', 1)
    size = request.args.get('size', 5)

    paginator = Item.query.paginate(page, size, False)
    result = categories_schema.dump(paginator.items)

    return {
        'data': result,
        'current_page': paginator.page,
        'per_page': paginator.per_page,
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
        raise NotFound(description='Item with this id doesn\'t exist.')
    else:
        return {
            'data': item_schema.dump(item)
        }


@item_api.route('', methods=['POST'])
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
    :return: id of the newly created item
    """
    body = request.get_json()
    body['creator_id'] = get_jwt_identity()

    item_schema.load(body)

    if Category.find_by_id(body['category_id']) is None:
        raise NotFound(description='Category with this id doesn\'t exist.')

    if Item.query.filter_by(title=body['title']).first():
        raise DuplicatedEntity(description='Item with this id exists.')

    item = Item(**body)
    item.save()

    return {
        'id': item.id
    }


@item_api.route('/<int:_id>', methods=['PUT'])
@jwt_required
def put(_id):
    """
    PUT method for Item
    :requires: the login-ed user must be the one created this item

    :param _id: ID of the item we want to update

    :bodyparam title: Title of the item
    :bodyparam description: Description of the item

    :raise ValidationError 400: if form is messed up
    :raise DuplicatedEntity 400: if there is a item with the title.
    :raise Unauthorized 401: If not login
    :raise Forbidden 403: If user tries to delete other user's items
    :raise NotFound 404: If category_id is not valid or item with id is not valid
    :return: id of the newly created item
    """
    body = request.get_json()
    body['creator_id'] = get_jwt_identity()

    category_id = body.get('category_id', None)
    if category_id and Category.find_by_id(category_id) is None:
        raise NotFound(description='Category with this id doesn\'t exist.')

    item = Item.find_by_id(_id)
    if item is None:
        raise NotFound(description='Item with this id doesn\'t exist.')
    else:
        ItemSchema(partial=True).load(body)
        if Item.query.filter_by(title=body['title']):
            raise DuplicatedEntity(description='Item with this title has already existed.')

        if item.creator_id != get_jwt_identity():
            abort(403)
        item.title = body.get('title', item.title)
        item.description = body.get('description', item.description)
        item.category_id = category_id or item.category_id

    item.save()

    return {
        'id': item.id
    }


@item_api.route('/<int:_id>', methods=['DELETE'])
@jwt_required
def delete(_id):
    """
    DELETE method for Item
    :param _id: ID of the item we want to delete

    :raise Unauthorized 401: If not login
    :raise Forbidden 403: If user tries to delete other user's items
    :raise Not Found 404: If item with that id doesn't exist
    :return: 204 response
    """
    item = Item.find_by_id(_id)
    if item is None:
        raise NotFound(description='Item with this id doesn\'t exist.')
    else:
        if item.creator_id != get_jwt_identity():
            abort(403)
        item.delete()

    return {}, 204
