from operator import truediv
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = "users"

    username = Column(String(100), primary_key=True, index=True)
    email = Column(String(100))
    fullname = Column(String(100))
    password = Column(String)
    contact = Column(String(100))
    image = Column(String)
    date_birth = Column(DateTime)
    description = Column(String(500))
    application = relationship("UserJob", backref="users")


class Job(Base):
    __tablename__ = "job"

    id = Column(Integer, primary_key=True, index=True)
    creator = Column(String, ForeignKey("users.username"))
    name = Column(String(100))
    latitude = Column(Integer)
    longitude = Column(Integer)
    location = Column(String(500))
    city = Column(String(100))
    province = Column(String(100))
    description = Column(String(500))
    contact = Column(String)
    num_participants = Column(Integer)
    wage = Column(Integer)
    image = Column(String)
    status = Column(String)
    applicants = relationship("UserJob", backref="job")


class UserJob(Base):
    __tablename__ = "userjob"

    job_id = Column(Integer, ForeignKey("job.id"), primary_key=True)
    username = Column(String, ForeignKey("users.username"), primary_key=True)
    status = Column(String)
    rating = Column(Integer)
    review = Column(String(500))
