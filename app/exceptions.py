from starlette import status
from fastapi import HTTPException

INVALID_CREDENTIALS = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)
