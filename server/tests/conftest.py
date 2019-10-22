from dotenv import load_dotenv
import pytest

from main.app import create_app
from main.db import db
from main.models.user import User

@pytest.fixture
def client():
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
    load_dotenv()

    app = create_app('testing')

    with app.test_client() as client:
        with app.app_context():
            db.init_app(app)

            db.drop_all()
            db.create_all()

            a = User(**{'email': 'admin@gmail.com', 'password': '123456'})
            a.save()

        yield client