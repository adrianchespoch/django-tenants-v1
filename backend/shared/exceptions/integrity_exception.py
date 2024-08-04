from .custom_exception import CustomException


class CustomIntegrityException(CustomException):
    def __init__(self, message: str = "Integrity Error"):
        super().__init__(message)
