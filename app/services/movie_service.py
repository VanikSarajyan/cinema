from sqlalchemy.orm import Session

from app.exceptions import MovieNotFoundException
from app.models import Movie
from app.schemas import MovieCreate, MovieUpdate


class MovieService:
    def __init__(self, db: Session) -> None:
        self._db = db
        self._model = Movie

    def get_all_movies(self, only_actives: bool = True) -> list[Movie]:
        if only_actives:
            return self._db.query(Movie).filter(Movie.active).all()
        return self._db.query(Movie).all()

    def get_movie_by_id(self, movie_id: int) -> Movie | None:
        return self._db.query(Movie).filter(Movie.id == movie_id).first()

    def create_new_movie(self, movie_data: MovieCreate) -> Movie:
        new_movie = Movie(**movie_data.model_dump())
        self._db.add(new_movie)
        self._db.commit()
        self._db.refresh(new_movie)
        return new_movie

    def update_movie(self, movie_id: int, movie_data: MovieUpdate) -> Movie:
        db_movie = self.get_movie_by_id(movie_id)

        if not db_movie:
            raise MovieNotFoundException()

        for key, value in movie_data.model_dump(exclude_unset=True).items():
            setattr(db_movie, key, value)

        self._db.commit()
        self._db.refresh(db_movie)
        return db_movie

    def delete_movie(self, movie_id: int) -> None:
        db_movie = self.get_movie_by_id(movie_id)

        if not db_movie:
            raise MovieNotFoundException()

        self._db.delete(db_movie)
        self._db.commit()
