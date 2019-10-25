from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from main.db import db
from main.errors import NotFound, DuplicatedEntity, Forbidden, StatusCodeEnum
from main.models.category import Category
from main.models.item import Item
from main.schemas.category import CategorySchema
from main.schemas.http import CategoryPaginationQuerySchema, PaginationResponseSchema
from main.utils.decorators import request_parser

category_api = Blueprint('category', __name__)

category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)


@category_api.route('/categories', methods=['GET'])
@request_parser(CategoryPaginationQuerySchema)
def get(query_params):
    """
    GET all method for Category

    :queryparam page: page that client wants to get, default = 1
    :queryparam per_page: item per page that client wants to get, default = 5

    :raise Validation Error 400: When client passes invalid value for page, per_page
    :return: List of categories, current_page, per_page, total.
    """
    paginator = Category.query.paginate(page=query_params['page'],
                                        per_page=query_params['per_page'], error_out=False)
    result = categories_schema.dump(paginator.items)
    raw_response = {
        'data': result,
        'page': paginator.page,
        'per_page': paginator.per_page,
        'total_items': paginator.total
    }
    return PaginationResponseSchema().dump(raw_response)


@category_api.route('/categories/<int:category_id>', methods=['GET'])
def get_one(category_id):
    """
    GET one method for Category
    :param category_id: id of the category want to get

    :raise Not Found 404: If category with that id doesn't exist
    :return: Category with that id
    """

    category = Category.find_by_id(category_id)
    if category is None:
        raise NotFound(error_message='Category with this id doesn\'t exist.')
    else:
        return {
            'data': category_schema.dump(category)
        }


@category_api.route('/categories', methods=['POST'])
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
        raise DuplicatedEntity(error_message='Category with this title has already existed.')

    category = Category(**body)
    category.save()

    return {
        'data': category_schema.dump(category)
    }


@category_api.route('/categories/<int:category_id>', methods=['PUT'])
@jwt_required
def put(category_id):
    """
    PUT method for Category
    :param category_id: ID of the category we want to update
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

    category = Category.find_by_id(category_id)
    if category is None:
        raise NotFound(error_message='Category with this id doesn\'t exist.')
    else:
        if creator_id != category.creator_id:
            raise Forbidden('You can\'t update other users\'s category')

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


@category_api.route('/categories/<int:category_id>', methods=['DELETE'])
@jwt_required
def delete(category_id):
    """
    DELETE method for Category
    :param category_id: ID of the category we want to delete

    :raise Unauthorized 401: If user is not login-ed
    :raise Forbidden 403: if user try to update other user's category
    :raise Not Found 404: If category with that id doesn't exist
    :return: 204 response
    """

    category = Category.find_by_id(category_id)

    if category is None:
        raise NotFound(error_message='Category with this id doesn\'t exist.')
    else:
        creator_id = get_jwt_identity()
        if creator_id != category.creator_id:
            raise Forbidden('You can\'t delete other users\'s category')
        db.session.query(Item).filter(Item.category_id == category_id).delete()
        category.delete()

    return {}, StatusCodeEnum.NO_CONTENT
