import functools

from flask import request


def request_parser(schemacls):
    def my_decorator(func):
        @functools.wraps(func)
        def in_func(*args, **kwargs):
            data = schemacls().load(request.args)
            return func(*args, query_params=data, **kwargs)

        return in_func

    return my_decorator
