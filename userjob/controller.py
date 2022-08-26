from fastapi import Depends, FastAPI, HTTPException, APIRouter, status
from sqlalchemy.orm import Session

from auth.auth_controller import get_current_user
from auth.auth_schemas import UserInDB

from . import repository, schemas
from job.repository import get_job_by_id, num_of_accepted_requests
from job.schemas import JobInDB
import models
from database import get_db

router = APIRouter(
    prefix="/api/v1",
    tags=["user-job"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.post("/userjob/", response_model=schemas.UserJobInDB)
def create_user_job(item: schemas.UserJob, current_user: UserInDB = Depends(get_current_user), db: Session = Depends(get_db)
                    ):
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

    item = schemas.UserJobInDB(
        **item.dict(), username=current_user.username)
    return repository.create_user_job(db=db, item=item)


@router.put("/userjob/{job_id}/{username}/status", response_model=schemas.UserJobInDB)
def update_user_job_status(new_item: schemas.UserJobStatus, job_id: int, username: str, current_user: UserInDB = Depends(get_current_user), db: Session = Depends(get_db)
                           ):
    if get_job_by_id(db, job_id).creator != current_user.username:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Anda tidak memiliki akses untuk mengubah data",
            headers={"WWW-Authenticate": "Bearer"},
        )
    item = repository.get_user_job_by_pk(db, job_id, username)
    item.status = new_item.status
    return repository.update_user_job(db=db, item=item)


@router.put("/userjob/{job_id}/{user_id}/review", response_model=schemas.UserJobInDB)
def update_user_job_review(new_item: schemas.UserJobReview, job_id: int, username: str, current_user: UserInDB = Depends(get_current_user), db: Session = Depends(get_db)
                           ):
    if get_job_by_id(db, job_id).creator != current_user.username:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Anda tidak memiliki akses untuk mengubah data",
            headers={"WWW-Authenticate": "Bearer"},
        )
    item: schemas.UserJobInDB = repository.get_user_job_by_pk(
        db, job_id, username)
    if item.status != schemas.Status.completed:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Tidak bisa mereview pekerjaan yang belum selesai",
            headers={"WWW-Authenticate": "Bearer"},
        )
    item.review = new_item.review
    new_item.rating = new_item.rating
    return repository.update_user_job(db=db, item=item)
