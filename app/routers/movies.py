from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Request
from starlette import status
from sqlalchemy.orm import Session

from app.database import get_db
from app.exceptions import MovieNotFoundException
from app.models import Movie, UserRole, User
from app.security import get_current_user_cookie
from app.services import MovieService
from app.schemas import MovieCreate, MovieUpdate
from app.template import templates
from app.utils import redirect_to_login


movies_router = APIRouter(prefix="/movies", tags=["Movies"])


@movies_router.get("/")
def get_movies(db: Session = Depends(get_db)):
    movie_servie = MovieService(db)
    return movie_servie.get_all_movies()


@movies_router.get("/movies-page")
def render_movies_page(
    request: Request, db: Annotated[Session, Depends(get_db)], user: Annotated[User, Depends(get_current_user_cookie)]
):
    if user is None:
        return redirect_to_login()

    movie_servie = MovieService(db)
    movies = movie_servie.get_all_movies(only_actives=user.role != UserRole.admin)
    return templates.TemplateResponse("movies.html", {"request": request, "movies": movies, "user": user})


@movies_router.get("/movie-create")
def create_movie_form(request: Request, user: Annotated[User, Depends(get_current_user_cookie)]):
    if user is None:
        return redirect_to_login()

    if user.role != UserRole.admin.value:
        raise HTTPException(status_code=403, detail="Not authorized")

    return templates.TemplateResponse("movie-create.html", {"request": request, "user": user})


@movies_router.get("/{movie_id}/edit")
def edit_movie(
    movie_id: int,
    request: Request,
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user_cookie)],
):
    if user.role != UserRole.admin.value:
        raise HTTPException(status_code=403, detail="Not authorized")

    movie_servie = MovieService(db)
    movie = movie_servie.get_movie_by_id(movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    return templates.TemplateResponse("movie-edit.html", {"request": request, "movie": movie, "user": user})


@movies_router.post("/")
def create_movie(
    movie: MovieCreate,
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user_cookie)],
):
    if user.role != UserRole.admin.value:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized action")

    movie_servie = MovieService(db)

    return movie_servie.create_new_movie(movie)


@movies_router.put("/{movie_id}")
def update_movie(
    movie_id: int,
    movie: MovieUpdate,
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user_cookie)],
):
    if user.role != UserRole.admin.value:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized action")

    movie_servie = MovieService(db)

    try:
        return movie_servie.update_movie(movie_id, movie)
    except MovieNotFoundException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")


@movies_router.delete("/{movie_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_movie(
    movie_id: int,
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user_cookie)],
):
    if user.role != UserRole.admin.value:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized action")

    movie_servie = MovieService(db)

    try:
        return movie_servie.delete_movie(movie_id)
    except MovieNotFoundException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")
