
from datetime import datetime
from typing import Union

from pydantic import BaseModel, Field, EmailStr

from userjob.schemas import UserJob, UserJobInDB


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


class UserBase(BaseModel):
    username: str = Field(..., max_length=100)
    email: str = Field(None, max_length=100)
    fullname: str = Field(..., max_length=100)
    contact: str = Field(None, max_length=100)
    image: str = Field(None, max_length=100)
    date_birth: datetime = Field(None)
    description: str = Field(None, max_length=500)


class UserRead(UserBase):
    application: list[UserJobInDB] = Field([])

    class Config:
        orm_mode = True


class UserInDB(UserBase):
    password: str

    class Config:
        orm_mode = True
