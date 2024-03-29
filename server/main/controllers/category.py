from flask import Blueprint, Response
from flask_jwt_extended import jwt_required, get_jwt_identity

from main.db import db
from main.errors import NotFound, DuplicatedEntity, Forbidden, StatusCodeEnum
from main.models.category import CategoryModel
from main.models.item import ItemModel
from main.schemas.category import CategorySchema
from main.schemas.request import BasePaginationQuerySchema
from main.schemas.response import create_pagination_response_schema
from main.utils.decorators.request_parser import request_parser
from main.utils.response_helpers import create_data_response

category_api = Blueprint('category', __name__)

category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)


@category_api.route('/categories', methods=['GET'])
@request_parser(query_schema=BasePaginationQuerySchema())
def get_categories(query_params):
    """
    Get all categories with pagination
    :param query_params:
    :queryparam page: page that client wants to get, default = 1
    :queryparam per_page: 'items' per page that client wants to get, default = 5

    :raise ValidationError 400: When client passes invalid value for page, per_page
    :return: List of categories, current_page, per_page, total.
    """
    paginator = CategoryModel.query.paginate(page=query_params['page'],
                                             per_page=query_params['per_page'], error_out=False)

    return create_pagination_response_schema(data_schema=categories_schema).dump(paginator)


@category_api.route('/categories/<int:category_id>', methods=['GET'])
def get_category(category_id):
    """
    Get the category by id
    :param category_id: id of the category want to get

    :raise Not Found 404: If category with that id doesn't exist
    :return: Category with that id
    """
    category = CategoryModel.find_by_id(category_id)
    if category is None:
        raise NotFound(error_message='Category with this id doesn\'t exist.')

    return create_data_response(category_schema.dump(category))


@category_api.route('/categories', methods=['POST'])
@jwt_required
@request_parser(body_schema=CategorySchema(exclude=['creator_id']))
def create_category(body_params):
    """
    Create a category
    :param body_params:
    :bodyparam title: Title of the category
    :bodyparam description: Description of the category

    :raise ValidationError 400: if form is messed up
    :raise DuplicatedEntity 400: If try to create an existed object
    :raise BadRequest 400: if the body mimetype is not JSON
    :raise Unauthorized 401: If user is not login-ed
    :return: the created category
    """
    if CategoryModel.query.filter_by(title=body_params['title']).first():
        raise DuplicatedEntity(error_message='Category with this title has already existed.')

    body_params['creator_id'] = get_jwt_identity()
    category = CategoryModel(**body_params)
    category.save()

    return create_data_response(category_schema.dump(category))


@category_api.route('/categories/<int:category_id>', methods=['PUT'])
@jwt_required
@request_parser(body_schema=CategorySchema(partial=True))  # partial is fine because fields have validate property
def update_category(category_id, body_params):
    """
    Update the category with id
    :param category_id: ID of the category we want to update
    :param body_params:
    :bodyparam title: Title of the category
    :bodyparam description: Description of the category

    :raise ValidationError 400: if form is messed up
    :raise DuplicatedEntity 400: if there is a category with the title
    :raise BadRequest 400: if the body mimetype is not JSON
    :raise Unauthorized 401: If user is not login-ed
    :raise Forbidden 403: if user try to update other user's category
    :raise Not Found 404: If category with that id doesn't exist
    :return: the updated category
    """
    category = CategoryModel.find_by_id(category_id)
    if category is None:
        raise NotFound(error_message='Category with this id doesn\'t exist.')

    creator_id = get_jwt_identity()
    if creator_id != category.creator_id:
        raise Forbidden(error_message='You can\'t update other users\'s category')

    title = body_params.get('title')
    description = body_params.get('description')
    if title:
        if CategoryModel.query.filter_by(title=title).first():
            raise DuplicatedEntity(error_message='There is already a category with this title.')
        category.title = title
    if description:
        category.description = description
    category.save()

    return create_data_response(category_schema.dump(category))


@category_api.route('/categories/<int:category_id>', methods=['DELETE'])
@jwt_required
def delete_category(category_id):
    """
    Delete the category with id
    :param category_id: ID of the category we want to delete

    :raise Unauthorized 401: If user is not login-ed
    :raise Forbidden 403: if user try to update other user's category
    :raise Not Found 404: If category with that id doesn't exist
    :return: 204 response
    """
    category = CategoryModel.find_by_id(category_id)
    if category is None:
        raise NotFound(error_message='Category with this id doesn\'t exist.')

    creator_id = get_jwt_identity()
    if creator_id != category.creator_id:
        raise Forbidden(error_message='You can\'t delete other users\'s category')

    db.session.query(ItemModel).filter(
            ItemModel.category_id == category_id).delete()  # delete all items in this category
    category.delete()

    return Response(status=StatusCodeEnum.NO_CONTENT)
