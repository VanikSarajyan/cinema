from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Request
from starlette import status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Room
from app.security import get_current_user_cookie, redirect_to_login, redirect_to
from app.template import templates


rooms_router = APIRouter(prefix="/rooms", tags=["Rooms"])


class RoomBase(BaseModel):
    name: str
    rows: int = Field(..., ge=1, le=15)
    columns: int = Field(..., ge=1, le=15)


@rooms_router.get("/")
def get_movies(db: Session = Depends(get_db)):
    return db.query(Room).all()


@rooms_router.get("/rooms-page")
def render_rooms_page(
    request: Request, db: Annotated[Session, Depends(get_db)], user: Annotated[dict, Depends(get_current_user_cookie)]
):
    if user is None:
        return redirect_to_login()

    rooms = db.query(Room).all()
    return templates.TemplateResponse("rooms.html", {"request": request, "rooms": rooms, "user": user})
