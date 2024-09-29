import logging
from typing import Annotated
from fastapi import Depends, Request, APIRouter, HTTPException
from fastapi.responses import HTMLResponse
from starlette import status
from sqlalchemy.orm import Session

from app.exceptions import InvalidScheduleException
from app.template import templates
from app.schemas import ScheduleCreate
from app.services import ScheduleService, RoomService, MovieService
from app.database import get_db
from app.models import UserRole
from app.security import get_current_user_cookie
from app.utils import redirect_to_login

schdeules_router = APIRouter(prefix="/schedules", tags=["Schedules"])


@schdeules_router.get("/create-page", response_class=HTMLResponse)
def render_create_schedule_page(
    request: Request,
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[dict, Depends(get_current_user_cookie)],
):
    if user is None:
        return redirect_to_login()

    if user.role != UserRole.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")

    return templates.TemplateResponse(
        "schedule-create.html",
        {
            "request": request,
            "user": user,
            "movies": MovieService(db).get_all_movies(),
            "rooms": RoomService(db).get_alls_rooms(),
        },
    )


@schdeules_router.post("/create")
def create_schedule(
    schedule_data: ScheduleCreate,
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[dict, Depends(get_current_user_cookie)],
):
    if user is None:
        return redirect_to_login()

    if user.role != UserRole.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")

    schedule_service = ScheduleService(db, RoomService(db))

    try:
        return schedule_service.create_schedule(schedule_data)
    except InvalidScheduleException as e:
        logging.error(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
