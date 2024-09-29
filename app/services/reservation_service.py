from sqlalchemy.orm import Session

from app.models import Reservation, Seat
from app.services import ScheduleService, RoomService
from app.exceptions import (
    ReservationAlreadyExistsException,
    ReservationNotFoundException,
    ScheduleNotFoundException,
    SeatNotFoundException,
)


class ReservationService:
    def __init__(self, db: Session, schedule_service: ScheduleService | None = None):
        self._db = db
        self.schedule_service = schedule_service or ScheduleService(db, RoomService(db))

    def create_reservation(self, user_id: int, schedule_id: int, seat_id: int) -> Reservation:
        seat = self._db.query(Seat).filter(Seat.id == seat_id).first()
        schedule = self.schedule_service.get_schedule_by_id(schedule_id)

        if not seat:
            raise SeatNotFoundException("Seat not found")
        if not schedule:
            raise ScheduleNotFoundException("Schedule not found")

        existing_reservation = (
            self._db.query(Reservation)
            .filter(Reservation.schedule_id == schedule_id, Reservation.seat_id == seat_id)
            .first()
        )

        if existing_reservation:
            raise ReservationAlreadyExistsException("This seat is already reserved for the selected schedule")

        reservation = Reservation(user_id=user_id, schedule_id=schedule_id, seat_id=seat_id)
        self._db.add(reservation)
        self._db.commit()
        self._db.refresh(reservation)

        return reservation

    def delete_reservation(self, reservation_id: int) -> None:
        reservation = self._db.query(Reservation).filter(Reservation.id == reservation_id).first()

        if not reservation:
            raise ReservationNotFoundException("Reservation not found")

        self._db.delete(reservation)
        self._db.commit()

    def get_user_reservations(self, user_id: int) -> list[Reservation]:
        reservations = self._db.query(Reservation).filter(Reservation.user_id == user_id).all()

        return reservations
