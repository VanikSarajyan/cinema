from sqlalchemy import Column, Integer, String, Enum, Text, Boolean
from app.database import Base
import enum


class UserRole(enum.Enum):
    admin = "admin"
    regular = "regular"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String)
    role = Column(Enum(UserRole), default=UserRole.regular.value)


class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    poster = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    active = Column(Boolean, nullable=False, default=True)
