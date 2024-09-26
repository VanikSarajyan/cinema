from fastapi import APIRouter, Request
from app.template import templates
from app.security import get_current_user, redirect_to_login

reservations_router = APIRouter(prefix="/reservations", tags=["Reservations"])


@reservations_router.get("/reservations-page")
def reservations(request: Request):
    try:
        user = get_current_user(request.cookies.get("access_token"))

        if user is None:
            return redirect_to_login()

        return templates.TemplateResponse("reservations.html", {"request": request, "user": user})

    except Exception:
        return redirect_to_login()
