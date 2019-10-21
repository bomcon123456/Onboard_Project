from flask import Blueprint, request, abort
from flask_jwt_extended import jwt_required, get_jwt_identity

from main.db import db
from main.errors import NotFound, DuplicatedEntity, FalseArguments
from main.models.category import Category
from main.models.item import Item
from main.schemas.category import CategorySchema
from main.utils.type_conversions import pagination_params_conversion

category_api = Blueprint('category', __name__)

category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)


@category_api.route('', methods=['GET'])
def get():
    """
    GET all method for Category

    :queryparam page: page that client wants to get, default = 1
    :queryparam per_page: item per page that client wants to get, default = 5

    :raise FalseArguments 400: When client passes invalid value for page, per_page
    :return: List of categories, current_page, per_page, total.
    """

    page = request.args.get('page', 1)
    per_page = request.args.get('per_page', 5)

    pagination_params = pagination_params_conversion(page, per_page)

    if pagination_params is None:
        raise FalseArguments(error_message='Please insert a positive number for page/per_page')

    paginator = Category.query.paginate(page=pagination_params[0],
                                        per_page=pagination_params[1], error_out=False)

    result = categories_schema.dump(paginator.items)
    return {
        'data': result,
        'page': paginator.page,
        'per_page': paginator.per_page,
        'total_items': paginator.total
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
        raise NotFound(error_message='Category with this id doesn\'t exist.')
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
    :raise Unauthorized 401: If user is not login-ed
    :return: the created category
    """

    body = request.get_json()
    body['creator_id'] = get_jwt_identity()

    category_schema.load(body)

    if Category.query.filter_by(title=body['title']).first():
        raise DuplicatedEntity(error_message='Category with this id has already existed.')

    category = Category(**body)
    category.save()

    return {
        'data': category_schema.dump(category)
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
    :raise DuplicatedEntity 400: if there is a category with the title.
    :raise Unauthorized 401: If user is not login-ed
    :raise Forbidden 403: if user try to update other user's category
    :raise Not Found 404: If category with that id doesn't exist
    :return: the updated category
    """

    body = request.get_json()

    creator_id = get_jwt_identity()

    category = Category.find_by_id(_id)
    if category is None:
        raise NotFound(error_message='Category with this id doesn\'t exist.')
    else:
        if creator_id != category.creator_id:
            abort(403)

        CategorySchema(partial=True).load(body)

        title = body.get('title', None)
        if title and Category.query.filter_by(title=title).first():
            raise DuplicatedEntity(error_message='There is already a category with this title.')

        category.title = title or category.title
        category.description = body.get('description', category.description)

    category.save()

    return {
        'data': category_schema.dump(category)
    }


@category_api.route('/<int:_id>', methods=['DELETE'])
@jwt_required
def delete(_id):
    """
    DELETE method for Category
    :param _id: ID of the category we want to delete

    :raise Unauthorized 401: If user is not login-ed
    :raise Forbidden 403: if user try to update other user's category
    :raise Not Found 404: If category with that id doesn't exist
    :return: 204 response
    """

    category = Category.find_by_id(_id)

    if category is None:
        raise NotFound(error_message='Category with this id doesn\'t exist.')
    else:
        creator_id = get_jwt_identity()
        if creator_id != category.creator_id:
            abort(403)
        db.session.query(Item).filter(Item.category_id == _id).delete()
        category.delete()

    return {}, 204
