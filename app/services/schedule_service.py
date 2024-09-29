from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.models import Schedule
from app.services import RoomService, MovieService
from app.schemas import ScheduleCreate
from app.exceptions import InvalidScheduleException, ScheduleNotFoundException


class ScheduleService:
    def __init__(self, db: Session, room_service: RoomService, movie_service: MovieService | None = None) -> None:
        self._db = db
        self._room_service = room_service
        self._movie_service = movie_service or MovieService(db)

    def get_all_schedules(self) -> list[Schedule]:
        return self._db.query(Schedule).all()

    def get_schedule_by_id(self, schedule_id: int) -> Schedule | None:
        return self._db.query(Schedule).filter(Schedule.id == schedule_id).first()

    def create_schedule(self, schedule_data: ScheduleCreate) -> Schedule:
        if not self._room_service.is_room_available(
            schedule_data.room_id,
            schedule_data.start_time,
            schedule_data.end_time,
        ):
            raise InvalidScheduleException(f"Room with id: {schedule_data.room_id} is already booked during this time.")

        self.validate_schedule_time(
            movie_duration_minutes=self._movie_service.get_movie_by_id(schedule_data.movie_id).duration,
            start_time=schedule_data.start_time,
            end_time=schedule_data.end_time,
        )

        schedule = Schedule(
            movie_id=schedule_data.movie_id,
            room_id=schedule_data.room_id,
            start_time=schedule_data.start_time,
            end_time=schedule_data.end_time,
        )
        self._db.add(schedule)
        self._db.commit()
        self._db.refresh(schedule)

        return schedule

    def validate_schedule_time(self, movie_duration_minutes: int, start_time: datetime, end_time: datetime) -> None:
        """
        Validate that the schedule time is appropriate for the movie duration.
        - The schedule duration must be at least the movie duration.
        - The schedule duration must not exceed the movie duration by more than 10 min,
        rounded to the nearest 10 minutes.
        """
        time_diff = end_time - start_time

        max_duration = timedelta(minutes=(round(movie_duration_minutes / 10) * 10) + 10)

        min_duration = timedelta(minutes=movie_duration_minutes)

        if time_diff < timedelta(0):
            raise InvalidScheduleException("End date and time can't be before start date and time")

        if time_diff < min_duration:
            raise InvalidScheduleException(
                f"The schedule time is too short. It must be at least {movie_duration_minutes} minutes long.",
            )

        if time_diff > max_duration:
            raise InvalidScheduleException(
                f"The schedule time is too long. It should not exceed {movie_duration_minutes} minutes"
                "by more than 10 minutes.",
            )

    def get_schedules_by_movie_id(self, movie_id: int) -> list[Schedule]:
        return self._db.query(Schedule).filter(Schedule.movie_id == movie_id).all()

    def get_schedules_by_room_id(self, room_id: int) -> list[Schedule]:
        return self._db.query(Schedule).filter(Schedule.room_id == room_id).all()

    def delete_schedule(self, schedule_id: int) -> None:
        schedule = self._db.query(Schedule).filter(Schedule.id == schedule_id).first()

        if not schedule:
            raise ScheduleNotFoundException("Schedule not found")

        self._db.delete(schedule)
        self._db.commit()
