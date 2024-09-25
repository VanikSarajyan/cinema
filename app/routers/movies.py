from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db

movies_router = APIRouter(prefix="/movies", tags=["Movies"])
