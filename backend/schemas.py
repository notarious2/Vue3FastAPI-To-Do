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
        from_attributes = True

class CreateTaskSchema(TaskBase):
    text: str
    priority: int


class TaskDisplay(TaskBase):
    user_id: str
    task_id: str
    class Config:
        from_attributes = True

class Task(TaskBase):
    task_id: str
    user_id: str


class TaskOptional(TaskBase):
    priority: Optional[int]
    date: Optional[date]
    text: Optional[str]
    completed: Optional[bool]
    class Config:
        from_attributes = True


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
    created_at: datetime

    class Config:
        orm_mode = True
