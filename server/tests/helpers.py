from main.db import db
from main.models.category import Category
from main.models.item import Item
from main.models.user import User


def create_user(email, password):
    """
    Create user and save to database
    :param email: A valid email
    :param password: A string length >=4
    :return: user object
    """
    user = User(email=email, password=password)
    user.save()

    return user


def create_category(title, description):
    """
    Create category and save to database
    :param title: A unique string length >=4
    :param description: A string length >=4
    :return: category object
    """
    category = Category(title=title, description=description)
    category.save()

    return category


def create_categories(categories):
    """
    Create user and save to database
    :param categories: list of categories (dict)
    """
    category_objs = [Category(**cat) for cat in categories]
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
    item = Item(title=title, description=description, category_id=cat_id)
    item.save()

    return item


def create_items(items):
    """
    Create items and save to database
    :param items: list of items (dict)
    """
    item_objs = [Item(**item) for item in items]
    db.session.bulk_save_objects(item_objs)
    db.session.commit()


def create_test_db():
    """
    Create some initial data for the database for unit testing:
    - 2 users: id=(1,2)
    - 2 categories: id=(1,2), each category is created by the corresponding user
    - 3 items: id=(1,2,3)
    :return:
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
    items = Item.query.filter_by(category_id=category_id).all()
    return items


def get_category_id_of_item(item_id):
    item = Item.query.get(item_id)
    return item.category.id


def get_user_email(user_id):
    user = User.query.get(user_id)
    return user.email
