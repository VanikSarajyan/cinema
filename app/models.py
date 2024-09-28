from sqlalchemy import Column, Integer, String, Enum, Text, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
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
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.regular.value)


class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    poster = Column(String, nullable=False)
    duration = Column(Integer, nullable=False)
    description = Column(Text, nullable=True)
    active = Column(Boolean, nullable=False, default=True)

    schedules = relationship("Schedule", back_populates="movie", cascade="all, delete-orphan")


class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    rows = Column(Integer, nullable=False)
    columns = Column(Integer, nullable=False)

    seats = relationship("Seat", back_populates="room", cascade="all, delete-orphan")
    schedules = relationship("Schedule", back_populates="room", cascade="all, delete-orphan")


class Seat(Base):
    __tablename__ = "seats"

    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, ForeignKey("rooms.id", ondelete="CASCADE"))
    row_number = Column(Integer, nullable=False)
    column_number = Column(Integer, nullable=False)

    room = relationship("Room", back_populates="seats")


class Schedule(Base):
    __tablename__ = "schedule"

    id = Column(Integer, primary_key=True, index=True)
    movie_id = Column(Integer, ForeignKey("movies.id", ondelete="CASCADE"))
    room_id = Column(Integer, ForeignKey("rooms.id", ondelete="CASCADE"))
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)

    movie = relationship("Movie", back_populates="schedules")
    room = relationship("Room", back_populates="schedules")
