from flask import Blueprint, request, abort
from flask_jwt_extended import jwt_required, get_jwt_identity

from utils.customexceptions import NotFound, DuplicatedEntity
from models.item import Item
from models.category import Category
from main.db import db
from schemas.category import CategorySchema

category_api = Blueprint('category', __name__)

category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)


@category_api.route('', methods=['GET'])
def get():
    """
    GET all method for Category

    :queryparam page: page that client wants to get, default = 1
    :queryparam size: item per page that client wants to get, default = 5

    :return: List of categories, current_page, per_page, total.
    """
    page = request.args.get('page', 1)
    size = request.args.get('size', 5)

    paginator = Category.query.paginate(page, size, False)

    result = categories_schema.dump(paginator.items)
    return {
        'data': result,
        'current_page': paginator.page,
        'per_page': paginator.per_page,
        'total': paginator.total
    }


@category_api.route('/<int:_id>/items', methods=['GET'])
def get_item_by_category(_id):
    """
    GET item by category

    :param _id: id of the category
    :queryparam page: page that client wants to get, default = 1
    :queryparam size: item per page that client wants to get, default = 5

    :return: List of items, current_page, per_page, total.
    """
    page = request.args.get('page', 1)
    size = request.args.get('size', 5)

    paginator = Item.query.filter_by(category_id=_id).paginate(page, size, False)
    result = categories_schema.dump(paginator.items)

    return {
        'data': result,
        'current_page': paginator.page,
        'per_page': paginator.per_page,
        'total': paginator.total
    }


@category_api.route('/<int:_id>', methods=['GET'])
def get_one(_id):
    """
    GET one method for Category
    :param _id: id of the category want to get

    :raise Not Found 404: If category with that id doesn't exist
    :return: Category with that id
    """

    category = Category.find_by_id(_id)
    if category is None:
        raise NotFound(description='Category with this id doesn\'t exist.')
    else:
        return {
            'data': category_schema.dump(category)
        }


@category_api.route('', methods=['POST'])
@jwt_required
def post():
    """
    POST method for Category
    :bodyparam title: Title of the category
    :bodyparam description: Description of the category

    :raise ValidationError 400: if form is messed up
    :raise DuplicatedEntity 400: If try to create an existed object.
    :return: id of the newly created category
    """
    body = request.get_json()
    body['creator_id'] = get_jwt_identity()

    category_schema.load(body)

    if Category.query.filter_by(title=body['title']).first():
        raise DuplicatedEntity(description='Category with this id has already existed.')

    category = Category(**body)
    category.save()

    return {
        'id': category.id
    }


@category_api.route('/<int:_id>', methods=['PUT'])
@jwt_required
def put(_id):
    """
    PUT method for Category
    :param _id: ID of the category we want to update
    :bodyparam title: Title of the category
    :bodyparam description: Description of the category

    :raise ValidationError 400: if form is messed up
    :raise Forbidden 403: if user try to update other user's category
    :return: id of the newly created category
    """
    body = request.get_json()

    creator_id = get_jwt_identity()

    category = Category.find_by_id(_id)
    if category is None:
        body['creator_id'] = creator_id
        category_schema.load(body)

        category = Category(**body)
    else:
        if creator_id != category.creator_id:
            abort(403)
        CategorySchema(partial=True).load(body)

        category.title = body.get('title', category.title)
        category.description = body.get('description', category.description)

    category.save()

    return {
        'id': category.id
    }


@category_api.route('/<int:_id>', methods=['DELETE'])
@jwt_required
def delete(_id):
    """
    DELETE method for Category
    :param _id: ID of the category we want to delete

    :raise Not Found 404: If category with that id doesn't exist
    :return: 204 response
    """
    category = Category.find_by_id(_id)
    if category is None:
        raise NotFound(description='Category with this id has already existed.')
    else:
        print('wtf')
        db.session.query(Item).filter(Item.category_id == _id).delete()
        category.delete(commit=False)
        db.session.commit()

    return {}, 204
