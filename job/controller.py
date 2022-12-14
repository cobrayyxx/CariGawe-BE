from fastapi import Depends, FastAPI, HTTPException, APIRouter, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from auth.auth_controller import get_current_active_user
from typing import Optional
from auth.auth_schemas import UserInDB

from . import repository, schemas
import models
from database import SessionLocal, engine, get_db

router = APIRouter(
    prefix="/api/v1",
    tags=["job"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.get("/job/", response_model=list[schemas.JobInDB])
def get_job(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = repository.get_job(db, skip=skip, limit=limit)
    res = []
    for item in items:
        res.append(schemas.JobInDB(
            **item.__dict__, applicants=item.applicants))
    return res


@router.get("/job/{job_id}", response_model=schemas.JobInDB)
def get_by_id(job_id: int, db: Session = Depends(get_db)):
    item = repository.get_job_by_id(db, job_id)
    return schemas.JobInDB(**item.__dict__, applicants=item.applicants)


@router.post("/job/", response_model=schemas.JobInDB)
def create_job(item: schemas.Job = Form(...), file: Optional[UploadFile] = File(None), current_user: UserInDB = Depends(get_current_active_user),  db: Session = Depends(get_db)):

    if file and file.filename != "":
        url_img = repository.upload_image(file)
    else:
        url_img = None

    item = schemas.JobInDB(
        **item.dict(), creator=current_user.username, image=url_img)
    return repository.create_job(db=db, item=item)


@router.put("/job/", response_model=schemas.JobInDB)
def update_job(item: schemas.JobUpdate = Form(...), file: Optional[UploadFile] = File(None), current_user: UserInDB = Depends(get_current_active_user), db: Session = Depends(get_db)):
    if file and file.filename != "":
        url_img = repository.upload_image(file)
        item.image = url_img

    return repository.update_job(db=db, item=item, current_user=current_user)
