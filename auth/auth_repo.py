from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from database import SessionLocal, engine, get_db
from . import auth_schemas
import models


def register(user: auth_schemas.UserInDB, db: Session):
    try:
        db_user = models.User(**user)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username sudah digunakan",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_certain_user(db: Session, username: str):
    user = db.query(models.User).filter(
        models.User.username == username).first()
    if user is not None:
        return auth_schemas.UserInDB.from_orm(user)
    else:
        return None


def read_user(username: str, db: Session):
    user = db.query(models.User).filter(
        models.User.username == username).first()
    if user is None:
        return user
    return auth_schemas.UserRead.from_orm(user)
