from flask import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity

from main.db import db
from main.errors import NotFound, DuplicatedEntity, Forbidden, StatusCodeEnum
from main.models.category import Category
from main.models.item import Item
from main.schemas.category import CategorySchema
from main.schemas.request import BasePaginationQuerySchema
from main.schemas.response import PaginationResponseSchema
from main.utils.decorators.request_parser import request_parser

category_api = Blueprint('category', __name__)

category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)


@category_api.route('/categories', methods=['GET'])
@request_parser(query_schema=BasePaginationQuerySchema())
def get_all_categories(query_params):
    """
    Get all categories with pagination

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
def get_one_category(category_id):
    """
    Get the category by id
    :param category_id: id of the category want to get

    :raise Not Found 404: If category with that id doesn't exist
    :return: Category with that id
    """
    category = Category.find_by_id(category_id)
    if category is None:
        raise NotFound(error_message='Category with this id doesn\'t exist.')

    return {
        'data': category_schema.dump(category)
    }


@category_api.route('/categories', methods=['POST'])
@jwt_required
@request_parser(body_schema=CategorySchema(exclude=['creator_id']))
def create_one_category(body_params):
    """
    Create a category
    :bodyparam title: Title of the category
    :bodyparam description: Description of the category

    :raise ValidationError 400: if form is messed up
    :raise DuplicatedEntity 400: If try to create an existed object.
    :raise Unauthorized 401: If user is not login-ed
    :return: the created category
    """
    if Category.query.filter_by(title=body_params['title']).first():
        raise DuplicatedEntity(error_message='Category with this title has already existed.')
    body_params['creator_id'] = get_jwt_identity()
    category = Category(**body_params)
    category.save()

    return {
        'data': category_schema.dump(category)
    }


@category_api.route('/categories/<int:category_id>', methods=['PUT'])
@jwt_required
@request_parser(body_schema=CategorySchema(partial=True))  # partial is fine because fields have validate property
def update_one_category(category_id, body_params):
    """
    Update the category with id
    :param category_id: ID of the category we want to update
    :param body_params:
    :bodyparam title: Title of the category
    :bodyparam description: Description of the category

    :raise ValidationError 400: if form is messed up
    :raise DuplicatedEntity 400: if there is a category with the title.
    :raise Unauthorized 401: If user is not login-ed
    :raise Forbidden 403: if user try to update other user's category
    :raise Not Found 404: If category with that id doesn't exist
    :return: the updated category
    """

    category = Category.find_by_id(category_id)
    if category is None:
        raise NotFound(error_message='Category with this id doesn\'t exist.')
    creator_id = get_jwt_identity()
    if creator_id != category.creator_id:
        raise Forbidden('You can\'t update other users\'s category')

    title = body_params.get('title')
    description = body_params.get('description')
    if title:
        if Category.query.filter_by(title=title).first():
            raise DuplicatedEntity(error_message='There is already a category with this title.')
        category.title = title
    if description:
        category.description = description
    category.save()

    return {
        'data': category_schema.dump(category)
    }


@category_api.route('/categories/<int:category_id>', methods=['DELETE'])
@jwt_required
def delete_one_category(category_id):
    """
    Delete the category with id
    :param category_id: ID of the category we want to delete

    :raise Unauthorized 401: If user is not login-ed
    :raise Forbidden 403: if user try to update other user's category
    :raise Not Found 404: If category with that id doesn't exist
    :return: 204 response
    """
    category = Category.find_by_id(category_id)
    if category is None:
        raise NotFound(error_message='Category with this id doesn\'t exist.')
    creator_id = get_jwt_identity()
    if creator_id != category.creator_id:
        raise Forbidden('You can\'t delete other users\'s category')
    
    db.session.query(Item).filter(Item.category_id == category_id).delete()  # delete all items in this category
    category.delete()

    return {}, StatusCodeEnum.NO_CONTENT
