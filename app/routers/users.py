from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from pydantic import BaseModel, EmailStr
from starlette import status
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from app.security import get_password_hash, verify_password, create_access_token
from app.template import templates

users_router = APIRouter(prefix="/users", tags=["Users"])


class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str
    verify_password: str


class Token(BaseModel):
    access_token: str
    token_type: str


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def authenticate_user(username: str, password: str, db):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


@users_router.get("/login-page")
def render_login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@users_router.post("/login", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Annotated[Session, Depends(get_db)]
):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user.")
    token = create_access_token(user.username, user.id, user.role.value)

    return {"access_token": token, "token_type": "bearer"}


@users_router.get("/register-page")
def render_register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@users_router.post("/register", response_model=Token)
def register(user_data: UserRegister, db: Session = Depends(get_db)):
    user = get_user_by_email(db, user_data.email)
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")

    if user_data.password != user_data.verify_password:
        raise HTTPException(status_code=400, detail="Password mismatch")

    hashed_password = get_password_hash(user_data.password)
    new_user = User(username=user_data.username, email=user_data.email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    access_token = create_access_token(new_user.username, new_user.id, new_user.role.value)
    return {"access_token": access_token, "token_type": "bearer"}
