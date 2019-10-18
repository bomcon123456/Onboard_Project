from flask import Blueprint, jsonify
from marshmallow import ValidationError
from sqlalchemy import exc


class MyBaseException(Exception):
    """
    BaseException class
    - Simply made to name each exception so we can handle exception more precise
    """
    status_code = 400

    def __init__(self, error_message, message='500_001', status_code=None):
        """
        Constructor
        :param message: the message that will be send to client when this is raised
        :param status_code: status_code of the response
        """
        super().__init__(self)
        self.message = message
        self.description = error_message
        if status_code is not None:
            self.status_code = status_code

    def to_response(self):
        """

        :return: Response to send to client with status_code
        """
        result = dict()
        result['error_code'] = self.message
        result['error_message'] = self.description
        return result, self.status_code


class NotFound(MyBaseException):
    """
    Not Found Exception
    - Will be raised when user try to access a entity does not exist in the database
    """

    def __init__(self, error_message, message='404_001'):
        super().__init__(error_message, message, status_code=404)


class FalseAuthentication(MyBaseException):
    """
    False Authentication Exception
    - Will be raised when user login with wrong value like password,...
    """

    def __init__(self, error_message, message='401_001'):
        super().__init__(error_message, message, status_code=401)


class FalseArguments(MyBaseException):
    """
    False Arguments Exception
    - Will be raised when client passes invalid query arguments
    """

    def __init__(self, error_message, message='400_003'):
        super().__init__(error_message, message, status_code=400)


class DuplicatedEntity(MyBaseException):
    """
    Duplicated Entity Exception
    - Will be raised when user try to create a new entity that violates unique property
    """

    def __init__(self, error_message, message='400_002'):
        super().__init__(error_message, message, status_code=400)


error_handlers = Blueprint('error_handlers', __name__)


@error_handlers.app_errorhandler(MyBaseException)
def handle_not_found(error):
    return error.to_response()


@error_handlers.app_errorhandler(403)
def handle_forbidden(error):
    response = jsonify({
        'error': '403_001',
        'error_message': 'You are not authorized to do this action.',
    })
    response.status_code = 403
    return response


@error_handlers.app_errorhandler(ValidationError)
def handle_invalid_form(error):
    response = jsonify({
        'error': '400_001',
        'error_message': error.messages,
    })
    response.status_code = 400
    return response


@error_handlers.app_errorhandler(exc.IntegrityError)
def handle_database_error(error):
    error_info = error.orig.args

    response = jsonify({
        'error': '500_002',
        'error_message': error_info[1]
    })
    return response, 500


@error_handlers.app_errorhandler(Exception)
def handle_all_errors(error):
    response = jsonify({
        'error': '500_001'
    })
    response.status_code = 500
    return response
