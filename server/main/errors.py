import logging
from enum import IntEnum

from flask import Blueprint, jsonify
from marshmallow import ValidationError
from sqlalchemy import exc


class StatusCodeEnum(IntEnum):
    OK = 200
    NO_CONTENT = 204
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    INTERNAL_SERVER_ERROR = 500


class ErrorCodeEnum(IntEnum):
    VALIDATION_ERROR = 400001
    DUPLICATED_ENTITY = 400002
    FALSE_AUTHENTICATION = 400003
    BAD_REQUEST = 400004
    NORMAL_FORBIDDEN = 403001
    NORMAL_NOT_FOUND = 404001
    INTERNAL_SERVER_ERROR = 500001
    INTERNAL_DATABASE_ERROR = 500002


class AppBaseException(Exception):
    """
    BaseException class (if we name the class BaseException, it will shadow the built-in exception)
    - Simply made to name each exception so we can handle exception more precise
    """
    status_code = StatusCodeEnum.INTERNAL_SERVER_ERROR

    def __init__(self, error_message='Something bad happened', error_code=ErrorCodeEnum.INTERNAL_SERVER_ERROR,
                 status_code=None):
        """
        Constructor
        :param error_code: The encoded code for the error we're raising
        :param error_message: The details of the error
        :param status_code: Status code of the response
        """
        super().__init__(self)
        self.error_code = error_code
        self.error_message = error_message
        if status_code is not None:
            self.status_code = status_code

    def to_response(self):
        """
        :return: Return a tuple consisting response body and its status code
        """
        result = {
            'error_code': self.error_code,
            'error_message': self.error_message
        }

        return result, self.status_code


class BadRequest(AppBaseException):
    """
    Bad Request Exception
    - Will be raised when client send a bad request generally (raised when doesnt match other 400xxx)
    """

    def __init__(self, error_message='Bad Request', error_code=ErrorCodeEnum.BAD_REQUEST):
        super().__init__(error_message, error_code, status_code=StatusCodeEnum.BAD_REQUEST)


class DuplicatedEntity(AppBaseException):
    """
    Duplicated Entity Exception
    - Will be raised when user try to create a new entity that violates unique property
    """

    def __init__(self, error_message='Duplicated Entity', error_code=ErrorCodeEnum.DUPLICATED_ENTITY):
        super().__init__(error_message, error_code, status_code=StatusCodeEnum.BAD_REQUEST)


class FalseAuthentication(AppBaseException):
    """
    False Authentication Exception
    - Will be raised when user login with wrong value like email, password
    """

    def __init__(self, error_message='False Authentication', error_code=ErrorCodeEnum.FALSE_AUTHENTICATION):
        super().__init__(error_message, error_code, status_code=StatusCodeEnum.BAD_REQUEST)


class Forbidden(AppBaseException):
    """
    Forbidden Exception
    - Will be raised when user try to manipulate other user's stuff
    """

    def __init__(self, error_message='Forbidden', error_code=ErrorCodeEnum.NORMAL_FORBIDDEN):
        super().__init__(error_message, error_code, status_code=StatusCodeEnum.FORBIDDEN)


class NotFound(AppBaseException):
    """
    Not Found Exception
    - Will be raised when user try to access an entity does not exist in the database
    """

    def __init__(self, error_message='Not Found', error_code=ErrorCodeEnum.NORMAL_NOT_FOUND):
        super().__init__(error_message, error_code, status_code=StatusCodeEnum.NOT_FOUND)


error_handlers = Blueprint('error_handlers', __name__)


@error_handlers.app_errorhandler(AppBaseException)
def handle_base_exception(error):
    return error.to_response()


@error_handlers.app_errorhandler(ValidationError)
def handle_invalid_form(error):
    response = jsonify({
        'error_code': ErrorCodeEnum.VALIDATION_ERROR,
        'error_message': error.messages,
    })

    return response, StatusCodeEnum.BAD_REQUEST


@error_handlers.app_errorhandler(exc.IntegrityError)
def handle_database_error(error):
    error_info = error.orig.args
    logging.error(error_info)
    response = jsonify({
        'error_code': ErrorCodeEnum.INTERNAL_DATABASE_ERROR,
        'error_message': error_info[1]
    })

    return response, StatusCodeEnum.INTERNAL_SERVER_ERROR


@error_handlers.app_errorhandler(Exception)
def handle_other_errors(error):
    logging.error(error)
    response = jsonify({
        'error_code': ErrorCodeEnum.INTERNAL_SERVER_ERROR,
        'error_message': 'Something bad happened.'
    })

    return response, StatusCodeEnum.INTERNAL_SERVER_ERROR
