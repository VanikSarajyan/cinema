from sqlalchemy import Column, Integer, String, Enum, Text, Boolean
from app.database import Base
import enum


class UserRole(enum.StrEnum):
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
    name = Column(String, nullable=False, unique=True)
    poster = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    active = Column(Boolean, nullable=False, default=True)


class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    rows = Column(Integer, nullable=False)
    columns = Column(Integer, nullable=False)

    @property
    def seats(self):
        return self.rows * self.columns
