from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette import status

from app.routers import movies_router, users_router, reservations_router, rooms_router, schdeules_router
from app.template import templates


def create_app():
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
    def render_reservations_page(request: Request):
        return RedirectResponse(url="/reservations/reservations-page", status_code=status.HTTP_302_FOUND)

    app.include_router(movies_router)
    app.include_router(users_router)
    app.include_router(reservations_router)
    app.include_router(rooms_router)
    app.include_router(schdeules_router)

    @app.exception_handler(404)
    def custom_404_handler(request, _):
        return templates.TemplateResponse("404.html", {"request": request}, status_code=status.HTTP_404_NOT_FOUND)

    return app


app = create_app()

if __name__ == "__main__":
    # For Debugging
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=80, reload=True)
