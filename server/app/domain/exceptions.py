class AppException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class NotFoundException(AppException):
    def __init__(self, message: str = "Resource not found"):
        self.message = message
        super().__init__(self.message)


class AuthenticateException(AppException):
    def __init__(self, message: str = "Error to Authenticate"):
        self.message = message
        super().__init__(self.message)
