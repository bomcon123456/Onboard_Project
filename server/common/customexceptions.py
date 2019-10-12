class MyBaseException(Exception):
    status_code = 400

    def __init__(self, message='Exception raised', status_code=None):
        super().__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code

    def to_response(self):
        result = dict()
        result['message'] = self.message
        return result, self.status_code


class NotFound(MyBaseException):
    def __init__(self, message='Can not find the specified entity.'):
        super().__init__(message, status_code=404)
