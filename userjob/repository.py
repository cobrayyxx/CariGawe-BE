from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from database import SessionLocal, engine, get_db
from job.repository import get_job_by_id, num_of_accepted_requests
from job.schemas import JobInDB
from . import schemas
import models
import psycopg2
from psycopg2 import errors


def get_user_job_by_pk(db: Session, job_id: int, username: str):
    return db.query(models.UserJob).filter(models.UserJob.username == username, models.UserJob.job_id == job_id).first()


def create_user_job(db: Session, item: schemas.UserJob):
    db_job: JobInDB = get_job_by_id(db, item.job_id)
    if db_job.status == 'closed':
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Lowongan sudah ditutup",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if num_of_accepted_requests(db_job) >= db_job.num_participants:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Lowongan sudah penuh",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        db_item = models.UserJob(**item.dict())

        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item
    except IntegrityError as e:
        try:
            raise e.orig
        except errors.UniqueViolation:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Anda sudah mendaftar ke lowongan ini",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except errors.ForeignKeyViolation:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Job dengan id {item.job_id} tidak ditemukan",
                headers={"WWW-Authenticate": "Bearer"},
            )


def update_user_job(db: Session, item: schemas.UserJobInDB):
    db_item: schemas.UserJobInDB = get_user_job_by_pk(
        db, item.job_id, item.username)
    if db_item is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Job id {item.job_id} dan username {item.username} tidak ditemukan",
            headers={"WWW-Authenticate": "Bearer"},
        )
    db_item.rating = item.rating
    db_item.review = item.review
    db_item.status = item.status

    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
