import logging
from typing import Annotated
from fastapi import APIRouter, Request, Depends, HTTPException
from starlette import status
from sqlalchemy.orm import Session

from app.template import templates
from app.security import get_current_user_cookie
from app.models import User
from app.utils import redirect_to_login
from app.services import RoomService, MovieService, ReservationService, ScheduleService
from app.schemas import ReservationCreate
from app.database import get_db
from app.exceptions import (
    ReservationAlreadyExistsException,
    ReservationNotFoundException,
    SeatNotFoundException,
    ScheduleNotFoundException,
)

reservations_router = APIRouter(prefix="/reservations", tags=["Reservations"])


@reservations_router.get("/reservations-page")
def reservations(request: Request, user: Annotated[User, Depends(get_current_user_cookie)]):
    if user is None:
        return redirect_to_login()

    return templates.TemplateResponse("reservations.html", {"request": request, "user": user})


@reservations_router.get("/reserve/{schedule_id}")
def render_reserve_seat_page(request: Request, schedule_id: int, db: Annotated[Session, Depends(get_db)]):
    room_service = RoomService(db)
    movie_service = MovieService(db)
    schedule_servie = ScheduleService(db, room_service=room_service, movie_service=movie_service)

    schedule = schedule_servie.get_schedule_by_id(schedule_id)
    if not schedule:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Schedule not found")

    seats_with_status = []
    for seat in schedule.room.seats:
        reserved = any(reservation.schedule_id == schedule_id for reservation in seat.reservations)
        seats_with_status.append({"seat": seat, "reserved": reserved})

    return templates.TemplateResponse(
        "seat-reservation.html",
        {
            "request": request,
            "movie": schedule.movie,
            "room": schedule.room,
            "schedule": schedule,
            "seats_with_status": seats_with_status,
            "reservations": schedule.reservations,
        },
    )


@reservations_router.post("/")
def create_reservation(
    reservation: ReservationCreate,
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user_cookie)],
):
    reservation_service = ReservationService(db)

    try:
        reservation_service.create_reservation(
            user_id=user.id,
            schedule_id=reservation.schedule_id,
            seat_id=reservation.seat_id,
        )
    except (SeatNotFoundException, ScheduleNotFoundException) as e:
        logging.error(e)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ReservationAlreadyExistsException as e:
        logging.error(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@reservations_router.delete("/{reservation_id}")
def delete_reservation(
    reservation_id: int,
    db: Annotated[Session, Depends(get_db)],
):
    reservation_service = ReservationService(db)

    try:
        reservation_service.delete_reservation(reservation_id)
    except ReservationNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
