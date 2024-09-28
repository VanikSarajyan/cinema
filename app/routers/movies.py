from fastapi import APIRouter, Depends, HTTPException, Request
from starlette import status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Movie, UserRole, User
from app.security import get_current_user_cookie, redirect_to_login, redirect_to
from app.template import templates
from typing import Annotated

movies_router = APIRouter(prefix="/movies", tags=["Movies"])


class MovieBase(BaseModel):
    name: str = Field(..., min_length=1)
    poster: str = Field(..., min_length=1)
    description: str | None = None


class MovieCreate(MovieBase):
    active: bool = True


class MovieUpdate(MovieBase):
    active: bool = True


@movies_router.get("/")
def get_movies(db: Session = Depends(get_db)):
    return db.query(Movie).filter(Movie.active).all()


@movies_router.get("/movies-page")
def render_movies_page(
    request: Request, db: Annotated[Session, Depends(get_db)], user: Annotated[User, Depends(get_current_user_cookie)]
):
    if user is None:
        return redirect_to_login()

    movies = db.query(Movie).all()
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

    movie = db.query(Movie).filter(Movie.id == movie_id).first()
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
    new_movie = Movie(**movie.model_dump())
    db.add(new_movie)
    db.commit()
    db.refresh(new_movie)
    return new_movie


@movies_router.put("/{movie_id}")
def update_movie(
    movie_id: int,
    movie: MovieUpdate,
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user_cookie)],
):
    if user.role != UserRole.admin.value:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized action")

    db_movie = db.query(Movie).filter(Movie.id == movie_id).first()

    if not db_movie:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")

    for key, value in movie.dict(exclude_unset=True).items():
        setattr(db_movie, key, value)

    db.commit()
    db.refresh(db_movie)
    return db_movie


@movies_router.delete("/{movie_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_movie(
    request: Request,
    movie_id: int,
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user_cookie)],
):
    if user.role != UserRole.admin.value:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized action")
    db_movie = db.query(Movie).filter(Movie.id == movie_id).first()

    if not db_movie:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")

    db.delete(db_movie)
    db.commit()
    return None
