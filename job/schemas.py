from enum import Enum
from typing import Union

from pydantic import BaseModel, Field

from userjob.schemas import UserJob, UserJobInDB


class Status(str, Enum):
    open = 'open'
    closed = 'closed'


class Job(BaseModel):
    description: str = Field(None, max_length=100)
    name: str = Field(..., max_length=100)
    latitude: int = Field(0)
    longitude: int = Field(0)
    location: str = Field(None, max_length=500)
    city: str = Field(None, max_length=100)
    province: str = Field(None, max_length=100)
    description: str = Field(None, max_length=500)
    contact: str = Field(None, max_length=100)
    num_participants: int = Field(...)
    wage: int = Field(...)
    image: str = Field(None)
    status: Status = Field(Status.open)

    class Config:
        orm_mode = True


class JobUpdate(Job):
    id: int = Field(None)

    class Config:
        orm_mode = True


class JobInDB(JobUpdate):
    applicants: list[UserJobInDB] = Field([])
    creator: str = Field(None)

    class Config:
        orm_mode = True
