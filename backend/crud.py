from operator import and_
from sqlalchemy.orm import Session
from sqlalchemy import and_
from sqlalchemy.sql import case
import models, schemas
import uuid
from password_hashing import Hash
from fastapi import HTTPException, status
from datetime import datetime
# TASK RELATED QUERIES

# need this function:
# - to check for duplicate Task IDs when creating a new task
# - to delete task by its id
def get_task_by_id(db: Session, id: str):
    return db.query(models.TaskModel).filter(models.TaskModel.task_id == id).first()

#add task for logged in user
def add_task(db: Session, task: schemas.TaskCreate, current_user: models.UserModel):
    task_id = str(uuid.uuid4())
    #checking existence of task id
    while get_task_by_id(db=db, id=task_id):
        task_id = uuid.uuid4()
    task = models.TaskModel(
        task_id=task_id,
        date = task.date,
        priority = task.priority,
        text = task.text,
        completed = task.completed,
        user_id = current_user.user_id) # need to assign user id

    db.add(task)
    db.commit()
    db.refresh(task)

# get all tasks of a LOGGED IN user
def get_tasks(db: Session, current_user: models.UserModel):
    return db.query(models.TaskModel).filter(models.TaskModel.user_id == current_user.user_id).all()

# get all tasks of all users
def get_all_tasks(db: Session):
    return db.query(models.TaskModel).all()

# delete task by id - must be logged in
def delete_task_by_id(db: Session, task_id: int, user_id:str):
    # first pull that task
    task = get_task_by_id(db=db, id=task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail = f"task with id {task_id} not found")
    # check current user id matches user id in task 
    if task.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
        detail = "Only Task Creator Can Delete Task")
    db.delete(task)
    db.commit()
    return "task deleted"

# delete all tasks for all users
def delete_all_tasks(db: Session):
    db.query(models.TaskModel).delete()
    db.commit()

# update text content of the particular task

def update_task(db: Session, task_id: int, new_task: schemas.TaskOptional, user_id: str):
    # retrieve the task
    task = get_task_by_id(db=db, id=task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail = f"task with id {task_id} not found")
    # task text can be updated by the user who created it
    if task.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
        detail = "Only Task Creator Can Delete Task")
    # can change text, priority and completed if passed
    if new_task.text: task.text = new_task.text 
    if new_task.priority: task.priority = new_task.priority 
    #need to be careful here as completed is BOOLEAN
    if new_task.completed!=None: task.completed = new_task.completed 
    db.commit()
    return "task updated!"

def update_task_order(db: Session, payload: dict, current_user: models.UserModel):
    # extract date from payload - which is the only key
    payload = payload['update']
    # Load ALL TASKS of the user for a SPECIFIC DATE
    tasks = db.query(models.TaskModel).filter(and_(models.TaskModel.user_id == current_user.user_id), \
        models.TaskModel.task_id.in_(payload))
    # Update multiple rows of Priority based on payload containing ID and PRIORITY to be assigned
    tasks.filter(models.TaskModel.task_id.in_(payload)) \
        .update({models.TaskModel.priority: case(payload, value=models.TaskModel.task_id)}, synchronize_session=False)
    db.commit()



# USER RELATED QUERIES

# we need this function to check for duplicate User IDs when creating a new user
def get_user_by_id(db: Session, id: str):
    return db.query(models.UserModel).filter(models.UserModel.user_id == id).first()

# need for user login and registration
def get_user_by_username(db: Session, username: str):
    return db.query(models.UserModel).filter(models.UserModel.username == username).first()

# need for registration - to check if email aready registered
def get_user_by_email(db: Session, email: str):
    return db.query(models.UserModel).filter(models.UserModel.email == email).first()

def add_user(db: Session, user: schemas.UserCreate):
    user_id =  str(uuid.uuid4())
    
    #checking if such ID already exists:
    while get_user_by_id(db=db, id = user_id):
        user_id =  str(uuid.uuid4())

    #hashing password
    password = Hash.get_hashed_password(user.password)
    
    #adding to Model - SQL table
    new_user = models.UserModel(
    user_id=user_id,
    email = user.email,
    name = user.name,
    username = user.username,
    password = password,
    created_at = datetime.now())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


#get all users
def get_users(db: Session):
    return db.query(models.UserModel).all()

# delete user by id

def delete_user_by_id(db: Session, user_id: str):
    user = db.query(models.UserModel).filter(models.UserModel.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail = f"user with id {user_id} is not found")
    db.delete(user)
    db.commit()
    return "user deleted"


# delete all users
def delete_all_users(db: Session):
    db.query(models.UserModel).delete()
    db.commit()