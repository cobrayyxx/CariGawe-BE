
from datetime import datetime
from typing import Union

from pydantic import BaseModel, Field, EmailStr

from userjob.schemas import UserJob, UserJobInDB
import json


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


class UserBase(BaseModel):
    email: str = Field(None, max_length=100)
    fullname: str = Field(..., max_length=100)
    contact: str = Field(None, max_length=100)
    date_birth: datetime = Field(None)
    description: str = Field(None, max_length=500)

    @classmethod
    def __get_validators__(cls):
        yield cls.validate_to_json

    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value


class UserRead(UserBase):
    username: str = Field(..., max_length=100)
    application: list[UserJobInDB] = Field([])
    image: str = Field(None, max_length=100)

    class Config:
        orm_mode = True


class UserInDB(UserBase):
    username: str = Field(..., max_length=100)
    password: str
    image: str = Field(None, max_length=100)

    class Config:
        orm_mode = True
