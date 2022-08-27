from enum import Enum
from typing import Union
import json
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
    status: Status = Field(Status.open)

    @classmethod
    def __get_validators__(cls):
        yield cls.validate_to_json

    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value

    class Config:
        orm_mode = True


class JobUpdate(Job):
    id: int = Field(None)
    image: str = Field(None)

    class Config:
        orm_mode = True


class JobInDB(JobUpdate):
    applicants: list[UserJobInDB] = Field([])
    creator: str = Field(None)


    class Config:
        orm_mode = True
