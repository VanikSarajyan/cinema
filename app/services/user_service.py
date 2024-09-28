from sqlalchemy.orm import Session

from app.models import User
from app.security import verify_password, get_password_hash
from app.exceptions import PasswordMismatchException
from app.schemas import UserRegister


class UserService:
    def __init__(self, db: Session) -> None:
        self._db = db
        self._model = User

    def get_user_by_email(self, email: str) -> User | None:
        return self._db.query(User).filter(User.email == email).first()

    def get_user_by_username(self, username: str) -> User | None:
        return self._db.query(User).filter(User.username == username).first()

    def authenticate_user(self, username: str, password: str) -> User | None:
        user = self.get_user_by_username(username)
        if user and verify_password(password, user.hashed_password):
            return user

    def create_user(self, user_data: UserRegister) -> User:
        if user_data.password != user_data.verify_password:
            raise PasswordMismatchException()

        hashed_password = get_password_hash(user_data.password)
        new_user = User(username=user_data.username, email=user_data.email, hashed_password=hashed_password)
        self._db.add(new_user)
        self._db.commit()
        self._db.refresh(new_user)
        return new_user
