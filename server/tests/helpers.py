from main.db import db
from main.errors import StatusCodeEnum
from main.models.category import CategoryModel
from main.models.item import ItemModel
from main.models.user import UserModel


def create_user(email, password):
    """
    Create user and save to database
    :param email: A valid email
    :param password: A string length >=4
    :return: user object
    """
    user = UserModel(email=email, password=password)
    user.save()

    return user


def create_category(title, description):
    """
    Create category and save to database
    :param title: A unique string length >=4
    :param description: A string length >=4
    :return: category object
    """
    category = CategoryModel(title=title, description=description)
    category.save()

    return category


def create_categories(categories):
    """
    Create user and save to database
    :param categories: list of categories (dict)
    """
    category_objs = [CategoryModel(**cat) for cat in categories]
    db.session.bulk_save_objects(category_objs)
    db.session.commit()


def create_item(title, description, cat_id):
    """
    Create user and save to database
    :param title: A unique string length >=4
    :param description: A string length >=4
    :param cat_id: category id
    :return: category object
    """
    item = ItemModel(title=title, description=description, category_id=cat_id)
    item.save()

    return item


def create_items(items):
    """
    Create items and save to database
    :param items: list of items (dict)
    """
    item_objs = [ItemModel(**item) for item in items]
    db.session.bulk_save_objects(item_objs)
    db.session.commit()


def create_test_db():
    """
    Create some initial data for the database for unit testing:
    - 2 users: id=(1,2)
    - 2 categories: id=(1,2), each category is created by the corresponding user
    - 3 items: id=(1,2,3)
    :return: Identifier of the user we use for authentication
    """
    client_user = create_user('admin@gmail.com', '123456')
    other_user = create_user('user@gmail.com', '123456')

    create_categories(
            [{'title': 'Minecraft', 'description': 'Minecraft stuffs', 'creator_id': client_user.id},
             {'title': 'Seafood', 'description': 'Seafood stuffs', 'creator_id': other_user.id}])

    create_items(
            [
                {
                    'title': 'Minecraft Sword', 'description': 'Sharpy', 'category_id': 1,
                    'creator_id': client_user.id
                },
                {
                    'title': 'Minecraft Dirt Block', 'description': 'Very dull...', 'category_id': 1,
                    'creator_id': client_user.id
                },
                {
                    'title': 'Crab', 'description': 'Crabby...', 'category_id': 1,
                    'creator_id': other_user.id
                }
            ])

    return client_user.id


def get_items_by_category_id(category_id):
    items = ItemModel.query.filter_by(category_id=category_id).all()
    return items


def get_category_id_of_item(item_id):
    item = ItemModel.query.get(item_id)
    return item.category.id


def get_user_email(user_id):
    user = UserModel.query.get(user_id)
    return user.email


def get_item_by_id(item_id):
    item = ItemModel.query.get(item_id)
    return item


def get_category_by_id(category_id):
    category = CategoryModel.query.get(category_id)
    return category


def assert_item_create_update_no_exceptions(test_status_code, test_data, test_category, goal_title, goal_description,
                                            goal_category_id):
    assert test_status_code == StatusCodeEnum.OK
    assert test_data
    assert test_data.get('title') == goal_title
    assert test_data.get('description') == goal_description
    assert test_category
    assert test_category.get('id') == goal_category_id


def assert_status_error_code(test_status_code, test_error_code, goal_status_code, goal_error_code):
    assert test_status_code == goal_status_code
    assert test_error_code == goal_error_code


def assert_pagination_response(test_status_code, test_data, test_total_items, test_page, test_per_page,
                               goal_status_code, goal_total_items, goal_page, goal_per_page, goal_data_length=None):
    assert test_status_code == goal_status_code
    assert test_data is not None
    if goal_data_length:
        assert len(test_data) == goal_data_length
    assert test_total_items == goal_total_items
    assert test_page == goal_page
    assert test_per_page == goal_per_page
