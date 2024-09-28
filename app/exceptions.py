from starlette import status
from fastapi import HTTPException


class UserNotFoundException(Exception):
    pass


class PasswordMismatchException(Exception):
    pass


class MovieNotFoundException(Exception):
    pass
