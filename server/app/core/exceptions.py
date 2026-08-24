class AppException(Exception):
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class NotFoundException(Exception):
    def __init__(self, message: str = "Resource not found"):
        self.message = message
        self.status_code = 404
        super().__init__(self.message, self.status_code)
