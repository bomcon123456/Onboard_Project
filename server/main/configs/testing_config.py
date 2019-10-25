import os

from main.configs.base_config import BaseConfig


class TestingConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TESTING_DATABASE_URL')
