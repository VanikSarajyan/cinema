from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette import status

from app.database import engine
from app.models import Base
from app.routers import movies_router, users_router, reservations_router
from app.template import templates


# Create tables
# Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def main(request: Request):
    return RedirectResponse(url="/reservations", status_code=status.HTTP_302_FOUND)


app.include_router(movies_router)
app.include_router(users_router)
app.include_router(reservations_router)


@app.exception_handler(404)
async def custom_404_handler(request, _):
    return templates.TemplateResponse("404.html", {"request": request})
