class MyBaseException(Exception):
    """
    BaseException class
    - Simply made to name each exception so we can handle exception more precise
    """
    status_code = 400

    def __init__(self, description, message='Exception raised', status_code=None):
        """
        Constructor
        :param message: the message that will be send to client when this is raised
        :param status_code: status_code of the response
        """
        super().__init__(self)
        self.message = message
        self.description = description
        if status_code is not None:
            self.status_code = status_code

    def to_response(self):
        """

        :return: Response to send to client with status_code
        """
        result = dict()
        result['message'] = self.message
        result['description'] = self.description
        return result, self.status_code


class NotFound(MyBaseException):
    """
    Not Found Exception
    - Will be raised when user try to access a entity does not exist in the database
    """

    def __init__(self, description, message='Not Found.'):
        super().__init__(description, message, status_code=404)


class FalseAuthentication(MyBaseException):
    """
    False Authentication Exception
    - Will be raised when user login with wrong value like password,...
    """

    def __init__(self, description, message='False Authentication.'):
        super().__init__(description, message, status_code=400)


class DuplicatedEntity(MyBaseException):
    """
    Duplicated Entity Exception
    - Will be raised when user try to create a new entity that violates unique property
    """

    def __init__(self, description, message='Duplicated Entity.'):
        super().__init__(description, message, status_code=400)
