from enum import Enum
from typing import Optional, Union

from pydantic import BaseModel, Field


class Status(str, Enum):
    requested = 'requested'
    accepted = 'accepted'
    completed = 'completed'
    rejected = 'rejected'


class UserJob(BaseModel):
    job_id: int = Field(...)

    class Config:
        orm_mode = True


class UserJobInDB(UserJob):
    username: str = Field(...)
    status: Status = Field(Status.requested)
    rating: int = Field(0)
    review: Optional[str] = Field("", max_length=500)

    class Config:
        orm_mode = True


class UserJobStatus(BaseModel):
    status: str = Field("requested")

    class Config:
        orm_mode = True


class UserJobReview(BaseModel):
    rating: int = Field(0)
    review: str = Field("", max_length=500)

    class Config:
        orm_mode = True
