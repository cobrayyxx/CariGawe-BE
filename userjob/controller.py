from fastapi import Depends, FastAPI, HTTPException, APIRouter, status
from sqlalchemy.orm import Session

from auth.auth_controller import get_current_user
from auth.auth_schemas import UserInDB

from . import repository, schemas
from job import repository as job_repository
import models
from database import SessionLocal, engine, get_db

router = APIRouter(
    prefix="/api/v1",
    tags=["user-job"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.post("/userjob/", response_model=schemas.UserJobInDB)
def create_user_job(item: schemas.UserJob, current_user: UserInDB = Depends(get_current_user), db: Session = Depends(get_db)
                    ):
    item = schemas.UserJobInDB(
        **item.dict(), username=current_user.username)
    return repository.create_user_job(db=db, item=item)


# TODO
@router.put("/userjob/{job_id}/{user_id}/status", response_model=schemas.UserJobInDB)
def update_user_job_status(item: schemas.UserJobInDB, current_user: UserInDB = Depends(get_current_user), db: Session = Depends(get_db)
                           ):
    # if job_repository.get_job_by_id(item.job_id) != current_user.username:
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         detail="Anda tidak memiliki akses untuk mengubah data",
    #         headers={"WWW-Authenticate": "Bearer"},
    #     )

    return repository.update_user_job(db=db, item=item)


@router.put("/userjob/{job_id}/{user_id}/review", response_model=schemas.UserJobInDB)
def update_user_job_review(item: schemas.UserJobInDB, current_user: UserInDB = Depends(get_current_user), db: Session = Depends(get_db)
                           ):
    # if job_repository.get_job_by_id(item.job_id) != current_user.username:
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         detail="Anda tidak memiliki akses untuk mengubah data",
    #         headers={"WWW-Authenticate": "Bearer"},
    #     )

    return repository.update_user_job(db=db, item=item)
