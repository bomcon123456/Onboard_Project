class MyBaseException(Exception):
    """
    BaseException class
    - Simply made to name each exception so we can handle exception more precise
    """
    status_code = 400

    def __init__(self, message='Exception raised', status_code=None):
        """
        Constructor
        :param message: the message that will be send to client when this is raised
        :param status_code: status_code of the response
        """
        super().__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code

    def to_response(self):
        """

        :return: Response to send to client with status_code
        """
        result = dict()
        result['message'] = self.message
        return result, self.status_code


class NotFound(MyBaseException):
    """
    Not Found Exception
    - Will be raised when user try to access a entity does not exist in the database
    """
    def __init__(self, message='Can not find the specified entity.'):
        super().__init__(message, status_code=404)
