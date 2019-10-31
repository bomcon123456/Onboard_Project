import functools

from flask import request

from main.errors import BadRequest


def request_parser(query_schema=None, body_schema=None):
    """
    Decorator used for request parsing
    :param body_schema: Schema for request's query params
    :param query_schema: Schema for request's body params
    :param schemacls: Schema Class to parse request
    :return: return response for Flask
    """

    def my_decorator(func):
        @functools.wraps(func)
        def in_func(*args, **kwargs):
            query_params = body_params = None

            if query_schema is not None:
                query_params = query_schema.load(request.args)
            if body_schema is not None:
                # If the mimetype does not indicate JSON this returns None, silent=True make is return None if
                # JSON-type body is not correct.
                json_data = request.get_json(silent=True)
                if json_data is None:
                    raise BadRequest(error_message='Please send a request consisting JSON body type.')
                body_params = body_schema.load(json_data)

            if query_params is not None:
                kwargs['query_params'] = query_params
            if body_params is not None:
                kwargs['body_params'] = body_params

            return func(*args, **kwargs)

        return in_func

    return my_decorator
