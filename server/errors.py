class APIException(Exception):
    status_code: int = 0

    def __init__(self, message: str, status_code: int = None):
        Exception.__init__(self)
        self.message = message
        if status_code:
            self.status_code = status_code

    @property
    def json(self):
        return {'error': {'code': self.status_code, 'message': self.message}}


class UserCodeException(APIException):
    status_code = 1001
