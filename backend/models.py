from email.policy import default
from sqlalchemy import Column, Date, Integer, String, Boolean, ForeignKey, DateTime
from database import Base
from sqlalchemy.orm import relationship

class UserModel(Base):
    __tablename__ = "user"
    user_id = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String, index=False)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    created_at = Column(DateTime)
    todos = relationship("TaskModel", back_populates = "owner")

class TaskModel(Base):
    __tablename__ = "task"
    task_id = Column(String, primary_key=True, index=True, unique=True)
    priority = Column(Integer)
    date = Column(Date)
    text = Column(String, nullable=False)
    completed = Column(Boolean, default=False) #need to use default otherwise result is None
    user_id = Column(String, ForeignKey("user.user_id"))

    owner = relationship("UserModel", back_populates = "todos")

