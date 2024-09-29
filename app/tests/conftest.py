from datetime import datetime
import pytest
from fastapi import Depends
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.main import create_app
from app.database import Base, get_db
from app.models import Seat, Schedule, User, Movie, Room
from app.security import get_current_user_cookie


SQLALCHEMY_DATABASE_URL = "sqlite:///.test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


def mock_get_current_user_cookie(db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == "test@example.com").first()

    if not user:
        user = User(
            id=1,
            email="test@example.com",
            username="test_user",
            hashed_password="fakehashedpassword",
        )
        db.add(user)
        db.commit()

    return user


@pytest.fixture(scope="module")
def setup_database():
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()

    user = User(
        id=1,
        username="test_user",
        email="test@example.com",
        hashed_password="fakehashedpassword",
        role="regular",
    )

    movie = Movie(
        id=1,
        name="Test Movie",
        poster="test_movie.jpg",
        duration=120,
        active=True,
        description="Test movie description",
    )

    room = Room(id=1, name="Room 1", rows=5, columns=5)

    seat1 = Seat(id=1, row_number=1, column_number=1, room_id=1)
    seat2 = Seat(id=2, row_number=1, column_number=2, room_id=1)

    start_time = datetime.strptime("2024-10-01 14:00:00", "%Y-%m-%d %H:%M:%S")
    end_time = datetime.strptime("2024-10-01 16:00:00", "%Y-%m-%d %H:%M:%S")

    schedule = Schedule(id=1, movie_id=1, room_id=1, start_time=start_time, end_time=end_time)

    db.add(user)
    db.add(room)
    db.add(movie)
    db.add(seat1)
    db.add(seat2)
    db.add(schedule)
    db.commit()

    yield db

    db.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def app():
    app = create_app()
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user_cookie] = mock_get_current_user_cookie
    return app


@pytest.fixture
def client(app):
    return TestClient(app)
