from fastapi import Depends, FastAPI

from auth import auth_controller
from job import controller as job_controller
from userjob import controller as user_job_controller
from sub_app2 import items
import models
from database import SessionLocal, engine
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(auth_controller.router)
app.include_router(job_controller.router)
app.include_router(user_job_controller.router)
## app.include_router(items.router)


origins = [
    'https://carigawe-be.herokuapp.com',
    'http://carigawe-be.herokuapp.com',
    "http://localhost",
    "http://localhost:8080",
    'http://localhost:3000/'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)