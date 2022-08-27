from typing import Optional
from fastapi import HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from database import SessionLocal, engine, get_db
from . import auth_schemas
import models
import cloudinary


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


def update_user(db: Session, item: auth_schemas.UserInDB):
    db_item = db.query(models.User).filter(
        models.User.username == item.username).first()
    for var, value in vars(item).items():
        setattr(db_item, var, value) if value or str(
            value) == 'False' else None

    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
