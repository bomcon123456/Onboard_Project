from flask import Blueprint, request

from .model import Category
from .schema import CategorySchema
from ..items.schema import ItemSchema

category_api = Blueprint('category', __name__)

category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)
items_schema = ItemSchema(many=True)


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


@category_api.route('/<int:id>', methods=['GET'])
def get_one(id):
    """
    GET one method for Category

    :raise: Not found
    :return: Category with that id
    """

    category = Category.find_by_id(id)
    if category is None:
        raise Exception()
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

    :raise: ValidationError if form is messed up
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


@category_api.route('/<int:id>', methods=['PUT'])
def put(id):
    """
    PUT method for Category
    :param id: ID of the category we want to update
    :bodyparam title: Title of the category
    :bodyparam description: Description of the category

    :raise: ValidationError if form is messed up
    :return: id of the newly created category
    """
    body = request.get_json()

    category_schema.load(body)

    category = Category.find_by_id(id)
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


@category_api.route('/<int:id>', methods=['DELETE'])
def delete(id):
    """
    DELETE method for Category
    :param id: ID of the category we want to delete

    :return: 204 response
    """
    category = Category.find_by_id(id)
    if category is None:
        return {
                   'message': 'This category doesn\'t exist.',
               }, 404
    else:
        category.delete()

    return {
               'message': 'Delete category successfully.',
           }, 204
