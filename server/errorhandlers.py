from flask import Blueprint, jsonify
from flask_jwt import JWTError
from marshmallow import ValidationError
from sqlalchemy import exc

from common.customexceptions import NotFound

error_handlers = Blueprint('error_handlers', __name__)


@error_handlers.app_errorhandler(NotFound)
def handle_not_found(error):
    return error.to_response()


@error_handlers.app_errorhandler(JWTError)
def handle_unauthorized(error):
    response = jsonify({
        'error': 'Unauthorized',
        'description': 'Please sign in to do this action.',
    })
    response.status_code = 401
    return response


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
        'error': 'Try to create a new entity that has already existed.',
        'description': error_info[1]
    })
    if error_info[0] == 1062:
        response.status_code = 400
    else:
        response.status_code = 500
    return response

# @error_handlers.app_errorhandler(Exception)
# def handle_all_errors(error):
#     response = jsonify({
#         'error': '[ERROR]: Internal Server Error.'
#     })
#     response.status_code = 500
#     return response
