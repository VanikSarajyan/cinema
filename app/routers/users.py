from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from starlette import status
from fastapi.security import OAuth2PasswordRequestForm

from app.security import create_access_token
from app.services import UserService
from app.template import templates
from app.database import get_db

from app.schemas import Token, UserRegister

users_router = APIRouter(prefix="/users", tags=["Users"])


@users_router.get("/login-page")
def render_login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@users_router.post("/login", response_model=Token)
def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Annotated[Session, Depends(get_db)]
):
    user_service = UserService(db)
    user = user_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user.")
    token = create_access_token(user.username, user.id, user.role.value)

    return Token(access_token=token, token_type="bearer")


@users_router.get("/register-page")
def render_register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@users_router.post("/register", response_model=Token)
def register(user_data: UserRegister, db: Annotated[Session, Depends(get_db)]):
    user_service = UserService(db)
    user = user_service.get_user_by_email(user_data.email) or user_service.get_user_by_username(user_data.username)
    if user:
        raise HTTPException(status_code=400, detail="User already registered")

    new_user = user_service.create_user(user_data)

    access_token = create_access_token(new_user.username, new_user.id, new_user.role.value)
    return Token(access_token=access_token, token_type="bearer")
