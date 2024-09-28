from typing import Annotated
from fastapi import APIRouter, Request, Depends

from app.template import templates
from app.security import get_current_user_cookie
from app.models import User
from app.utils import redirect_to_login

reservations_router = APIRouter(prefix="/reservations", tags=["Reservations"])


@reservations_router.get("/reservations-page")
def reservations(request: Request, user: Annotated[User, Depends(get_current_user_cookie)]):
    if user is None:
        return redirect_to_login()

    return templates.TemplateResponse("reservations.html", {"request": request, "user": user})
