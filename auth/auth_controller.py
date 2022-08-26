from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, HTTPException, APIRouter, UploadFile, File, status
from database import SessionLocal, engine, get_db
from . import auth_schemas
from . import auth_repo
from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from settings import token_settings
from typing import Union

router = APIRouter(
    prefix="/api/v1",
    tags=["users"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = token_settings.SECRET_KEY
ALGORITHM = token_settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = token_settings.ACCESS_TOKEN_EXPIRE_MINUTES


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(payload)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = auth_schemas.TokenData(username=username)
        print(token_data)
    except JWTError:
        raise credentials_exception
    user = auth_repo.get_certain_user(db=db, username=token_data.username)
    print(user)
    if user is None:
        raise credentials_exception
    return user


def get_current_active_user(current_user: auth_schemas.UserInDB = Depends(get_current_user)):
    # print("##############")
    # print(current_user)
    # if current_user.disabled:
    #     raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(username: str, password: str, db: Session = Depends(get_db)):
    user = auth_repo.get_certain_user(db, username)
    if user is None:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@router.post("/login", response_model=auth_schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register", response_model=auth_schemas.UserInDB)
def register_controller(user: auth_schemas.UserInDB, db: Session = Depends(get_db)):
    user_dict = user.dict()
    password = user_dict['password']
    user_dict['password'] = get_password_hash(password)
    print(user_dict)
    return auth_repo.register(user=user_dict, db=db)


@router.get("/user/{username}", response_model=auth_schemas.UserRead)
async def get_by_username(username: str, db: Session = Depends(get_db)):
    item = auth_repo.read_user(username, db)
    print(item)
    return item
