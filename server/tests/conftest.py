from dotenv import load_dotenv
import pytest
from flask_jwt_extended import create_access_token

from main.app import create_app
from main.db import db
from tests.helpers import create_user, create_test_db


@pytest.fixture
def plain_client():
    load_dotenv()

    app = create_app('testing')

    with app.test_client() as client:
        with app.app_context():
            db.init_app(app)

            db.drop_all()
            db.create_all()

        yield client


@pytest.fixture
def one_user_in_db_client():
    """
    This fixture create the database consisting one user
    :return:
    """
    load_dotenv()

    app = create_app('testing')

    with app.test_client() as client:
        with app.app_context():
            db.init_app(app)

            db.drop_all()
            db.create_all()

            create_user(email='admin@gmail.com', password='123456')

        yield client


@pytest.fixture
def auth_client():
    """
    This fixture provide a authorized client, with some initial database
    :return:
    """
    load_dotenv()

    app = create_app('testing')

    with app.test_client() as client:
        with app.app_context():
            db.init_app(app)

            db.drop_all()
            db.create_all()

            user_id = create_test_db()
            access_token = create_access_token(identity=user_id)
            client.environ_base['HTTP_AUTHORIZATION'] = 'Bearer ' + access_token

        yield client
