from flask import Blueprint, request

from common.customexceptions import NotFound
from .model import Category
from .schema import CategorySchema

category_api = Blueprint('category', __name__)

category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)


@category_api.route('', methods=['GET'])
def get():
    """
    GET all method for Category

    :queryparam page: page that client wants to get, default = 1
    :queryparam size: item per page that client wants to get, default = 5

    :return: List of categories, currentPage, perPage, total.
    """
    page = request.args.get('page', 1)
    size = request.args.get('size', 5)

    paginator = Category.query.paginate(page, size, False)

    result = categories_schema.dump(paginator.items)
    return {
        'message': 'Fetch categories successfully.',
        'data': result,
        'currentPage': paginator.page,
        'perPage': paginator.per_page,
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
        raise NotFound(message='Category with this id doesn\'t exist.')
    else:
        return {
            'message': 'Fetch category successfully.',
            'data': category_schema.dump(category)
        }


@category_api.route('', methods=['POST'])
def post():
    """
    POST method for Category
    :bodyparam title: Title of the category
    :bodyparam description: Description of the category

    :raise ValidationError 400: if form is messed up
    :return: id of the newly created category
    """
    body = request.get_json()

    category_schema.load(body)

    category = Category(**body)
    category.save()

    return {
        'message': 'Create category successfully.',
        'id': category.id
    }


@category_api.route('/<int:_id>', methods=['PUT'])
def put(_id):
    """
    PUT method for Category
    :param _id: ID of the category we want to update
    :bodyparam title: Title of the category
    :bodyparam description: Description of the category

    :raise ValidationError 400: if form is messed up
    :return: id of the newly created category
    """
    body = request.get_json()

    category_schema.load(body)

    category = Category.find_by_id(_id)
    if category is None:
        category = Category(**body)
    else:
        category.title = body.get('title', category.title)
        category.description = body.get('description', category.description)

    category.save()

    return {
        'message': 'Update category successfully.',
        'id': category.id
    }


@category_api.route('/<int:_id>', methods=['DELETE'])
def delete(_id):
    """
    DELETE method for Category
    :param _id: ID of the category we want to delete

    :raise Not Found 404: If category with that id doesn't exist
    :return: 204 response
    """
    category = Category.find_by_id(_id)
    if category is None:
        raise NotFound(message='Category with this id doesn\'t exist.')
    else:
        category.delete()

    return {
               'message': 'Delete category successfully.',
           }, 204
