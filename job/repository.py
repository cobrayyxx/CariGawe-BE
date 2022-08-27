from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from auth.auth_schemas import UserInDB
from database import SessionLocal, engine, get_db
from userjob.schemas import Status
from . import schemas
import models
import cloudinary
import cloudinary.uploader
from typing import Optional

def get_job(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    return db.query(models.Job).offset(skip).limit(limit).all()


def get_job_by_id(db: Session, job_id: int):
    return db.query(models.Job).filter(models.Job.id == int(job_id)).first()


def num_of_accepted_requests(job: schemas.JobInDB):
    count = 0
    for applicant in job.applicants:
        if applicant.status == Status.accepted:
            count += 1
    return count


def update_job(db: Session, item: schemas.Job, current_user: UserInDB):
    db_item: schemas.JobInDB = get_job_by_id(
        db, item.id)
    if db_item.creator != current_user.username:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Anda tidak memiliki akses untuk mengubah data",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if db_item is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Job id {item.job_id} tidak ditemukan",
            headers={"WWW-Authenticate": "Bearer"},
        )
    for var, value in vars(item).items():
        setattr(db_item, var, value) if value or str(
            value) == 'False' else None

    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def create_job(db: Session, item: schemas.Job):
    db_item = models.Job(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def upload_image(file: Optional[UploadFile] = File(None)):
    result = cloudinary.uploader.upload(file.file)
    url = result.get("url")
    return url