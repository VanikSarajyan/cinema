from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str
    verify_password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class MovieBase(BaseModel):
    name: str = Field(..., min_length=1)
    poster: str = Field(..., min_length=1)
    description: str | None = None
    duration: int = Field(default=120)


class MovieCreate(MovieBase):
    active: bool = True


class MovieUpdate(MovieBase):
    active: bool = True


class ScheduleCreate(BaseModel):
    movie_id: int
    room_id: int
    start_time: datetime
    end_time: datetime


class ReservationCreate(BaseModel):
    seat_id: int
    schedule_id: int
