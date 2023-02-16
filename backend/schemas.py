from datetime import date
from pydantic import BaseModel
from typing import Optional
from config import settings
from datetime import datetime


class TaskBase(BaseModel):
    priority: int
    date: date
    text: str
    completed: bool = False #default value show in fastapi docs
    class Config:
        orm_mode = True
class TaskCreate(TaskBase):
    pass

class TaskDisplay(TaskBase):
    user_id: str
    task_id: str
    class Config:
        orm_mode = True

class Task(TaskBase):
    task_id: str
    user_id: str
    # class Config:
    #     orm_mode = True

class TaskOptional(TaskBase):
    priority: Optional[int]
    date: Optional[date]
    text: Optional[str]
    completed: Optional[bool]
    class Config:
        orm_mode = True


class User(BaseModel):
    user_id: str
    name: str
    email: str
    username: str
    password: str
    created_at: datetime
    # class Config:
    #     orm_mode = True

class UserCreate(BaseModel):
    name: str
    email: str
    username: str
    password: str

    class Config:
        orm_mode = True

class UserDisplay(BaseModel):
    username: str
    email: str
    user_id: str
    created_at: datetime

    # makes links between User and UserDisplay schemas
    class Config:
        orm_mode = True


class Settings(BaseModel):
    authjwt_secret_key: str = str(settings.SECRET_KEY)
