from sqlalchemy.orm import Session
from sqlalchemy import and_, select, or_
from sqlalchemy.sql import case
import schemas
from models import User, Task
from schemas import UserCreate, CreateTaskSchema
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from utils import get_hashed_password


async def get_task_by_id(db_session: AsyncSession, id: int):
    task = await db_session.get(Task, id)
    return task

async def add_task(db_session: AsyncSession, create_task_schema: CreateTaskSchema, current_user: User):
        
    task = Task(
        priority = create_task_schema.priority,
        text = create_task_schema.text,
        user_id = current_user.user_id)

    db_session.add(task)
    await db_session.commit()
    return task

async def get_user_tasks(db_session: AsyncSession, current_user: User):
    result =  await db_session.execute(select(Task)).filter(Task.user_id == current_user.user_id)
    users = result.scalars().all()
    return users


async def delete_task(db_session: AsyncSession, task_id: int, user_id: int):
    result = await db_session.execute(select(Task).where(and_(Task.id == task_id, Task.user_id == user_id)))
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail = f"task with id {task_id} not found")
    await db_session.delete(task)
    await db_session.commit()



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

def update_task_order(db: Session, payload: dict, current_user: User):
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

async def get_user_by_id(db_session: AsyncSession, id: int):
      user = await db_session.get(User, id)
      return user


async def get_user_by_username_or_email(db_session: AsyncSession, username: str):
    result = await db_session.execute(select(User).where(or_(User.username == username), User.email == username))
    
    return result.scalar_one_or_none()

async def get_user_by_username(db_session: AsyncSession, username: str):
    result =  await db_session.execute(select(User).where(User.username == username))
    return result.scalar_one_or_none()

async def get_user_by_email(db_session: AsyncSession, email: str):
    result =  await db_session.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()


async def create_user(db_session: AsyncSession, user_schema: UserCreate) -> User:
    hashed_password = get_hashed_password(user_schema.password)

    user = User(email = user_schema.email, name = user_schema.name, username = user_schema.username, password = hashed_password)
    
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    return user


async def get_users(db_session: AsyncSession):
    result = await db_session.execute(select(User))
    return result.scalars().all()


async def delete_user_by_id(db_session: AsyncSession, user_id: int):
    user = await db_session.get(User, id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail = f"user with id {user_id} is not found")
    await db_session.delete(user)
    await db_session.commit()


async def delete_all_users(db_session: Session):
    result = await db_session.execute(select(User))
    users = result.scalars().all()

    await db_session.delete(users)
    await db_session.commit()