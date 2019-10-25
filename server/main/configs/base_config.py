import os


class BaseConfig:
    DEBUG = False
    TESTING = False

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    JWT_ERROR_MESSAGE_KEY = 'error_message'

    SECRET_KEY = os.environ.get('APP_SECRET_KEY')
