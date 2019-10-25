import functools

from flask import request


def request_parser(schemacls):
    """
    Decorator used for request parsing
    :param schemacls: Schema Class to parse request
    :return: return response for Flask
    """

    def my_decorator(func):
        @functools.wraps(func)
        def in_func(*args, **kwargs):
            data = schemacls().load(request.args)
            return func(*args, query_params=data, **kwargs)

        return in_func

    return my_decorator
