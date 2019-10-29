import os

from main.configs.base import BaseConfig


class TestingConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TESTING_DATABASE_URL')
