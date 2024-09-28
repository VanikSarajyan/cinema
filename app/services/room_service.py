from datetime import datetime
from sqlalchemy.orm import Session

from app.models import Room, Schedule


class RoomService:
    def __init__(self, db: Session) -> None:
        self._db = db

    def get_alls_rooms(self) -> list[Room]:
        return self._db.query(Room).all()

    def is_room_available(self, room_id: int, start_time: datetime, end_time: datetime) -> bool:
        """
        Check if the room is available between start_time and end_time.
        """
        conflicting_schedule = (
            self._db.query(Schedule)
            .filter(Schedule.room_id == room_id, Schedule.start_time < end_time, Schedule.end_time > start_time)
            .first()
        )
        return conflicting_schedule is None
