from fastapi import Depends, FastAPI, HTTPException, APIRouter, status
from sqlalchemy.orm import Session
from auth.auth_controller import get_current_active_user

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
    return items


@router.get("/job/{job_id}", response_model=schemas.JobInDB)
def get_by_id(job_id: int, db: Session = Depends(get_db)):
    items = repository.get_job_by_id(db, job_id)
    return items


@router.post("/job/", response_model=schemas.JobInDB)
def create_job(item: schemas.Job, current_user: UserInDB = Depends(get_current_active_user), db: Session = Depends(get_db)):
    item = schemas.JobInDB(**item.dict(), creator=current_user.username)
    return repository.create_job(db=db, item=item)


@router.put("/job/", response_model=schemas.JobInDB)
def update_job(item: schemas.JobUpdate, current_user: UserInDB = Depends(get_current_active_user), db: Session = Depends(get_db)):
    return repository.update_job(db=db, item=item, current_user=current_user)
