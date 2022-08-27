from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from settings import settings
from typing import Any
import cloudinary, os

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

cloudinary.config( 
    cloud_name = os.environ['CLOUDINARY_CLOUD_NAME'],
    api_key = os.environ['CLOUDINARY_API_KEY'],
    api_secret = os.environ['CLOUDINARY_API_SECRET'],
    secure = True
)


@as_declarative()
class Base:
    id: Any
    __name__: str

    #to generate tablename from classname
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
