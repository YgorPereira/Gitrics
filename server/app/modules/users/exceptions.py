from app.core.exceptions import NotFoundException


class UserNotFoundException(NotFoundException):
    def __init__(self):
        super().__init__("User not found")
