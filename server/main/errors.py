from flask import Blueprint, jsonify
from marshmallow import ValidationError
from sqlalchemy import exc

from main.utils.customexceptions import MyBaseException

error_handlers = Blueprint('error_handlers', __name__)


@error_handlers.app_errorhandler(MyBaseException)
def handle_not_found(error):
    return error.to_response()


@error_handlers.app_errorhandler(403)
def handle_forbidden(error):
    response = jsonify({
        'error': 'Forbidden',
        'description': 'You are not authorized to do this action.',
    })
    response.status_code = 403
    return response


@error_handlers.app_errorhandler(ValidationError)
def handle_invalid_form(error):
    response = jsonify({
        'error': 'Bad request form.',
        'description': error.messages,
    })
    response.status_code = 400
    return response


@error_handlers.app_errorhandler(exc.IntegrityError)
def handle_database_error(error):
    error_info = error.orig.args

    response = jsonify({
        'error': 'Internal Error',
        'description': error_info[1]
    })
    return response, 500


# @error_handlers.app_errorhandler(Exception)
# def handle_all_errors(error):
#     response = jsonify({
#         'error': '[ERROR]: Internal Server Error.'
#     })
#     response.status_code = 500
#     return response
