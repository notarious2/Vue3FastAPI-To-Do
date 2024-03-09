from sqlalchemy.orm import Session
from sqlalchemy import and_, select, or_, update, cast, Date
from models import User, Task
from schemas import UserCreate, CreateTaskSchema, UpdateTaskSchema
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from utils import get_hashed_password
from datetime import date


async def get_task_by_id(db_session: AsyncSession, id: int) -> Task | None:
    task = await db_session.get(Task, id)
    return task

async def get_tasks_by_date(db_session: AsyncSession, selected_date: date, current_user: User) -> list[Task]:
    statement = select(Task).where(and_(cast(Task.created_at, Date) == cast(selected_date, Date), Task.user_id == current_user.id)).order_by(Task.priority.asc())
    result = await db_session.execute(statement)
    tasks = result.scalars().all()  
    return tasks


async def create_task(db_session: AsyncSession, create_task_schema: CreateTaskSchema, current_user: User) -> Task:
    task = Task(
        priority = create_task_schema.priority,
        text = create_task_schema.text,
        user_id = current_user.id)

    db_session.add(task)
    await db_session.commit()
    await db_session.refresh(task)
    return task

async def get_user_tasks(db_session: AsyncSession, current_user: User):
    result =  await db_session.execute(select(Task)).filter(Task.user_id == current_user.id)
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


async def update_task(db_session: AsyncSession, task: Task, new_task: UpdateTaskSchema) -> Task:
    if new_task.text: task.text = new_task.text 
    if new_task.priority: task.priority = new_task.priority 
    if new_task.completed is not None:
        task.completed = new_task.completed

    await db_session.commit()
    await db_session.refresh(task)
    
    return task


async def bulk_update_priorities(db_session: AsyncSession, priorities: dict[int, int], current_user: User):
    """
    priorities hold id:new_priority key-pair dictonary
    """
    # make sure all tasks (ids) belong to the current user
    result = await db_session.execute(select(Task.id).where(and_(Task.user_id == current_user.id, Task.id.in_(priorities))))
    task_ids = result.scalars().all() # returns list of ids

    # task ids provided doesn't match task ids found for user
    if not len(priorities) == len(task_ids):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Provided ids doesn't match tasks of the user [{priorities}]")

    # unpack into {id: key, priority:value} list
    priorities_to_update = [{"id": id, "priority": priority} for id, priority in priorities.items()]

    await db_session.execute(update(Task), priorities_to_update)
    await db_session.commit()


async def get_user_by_id(db_session: AsyncSession, id: int):
      user = await db_session.get(User, id)
      return user


async def get_user_by_username_or_email(db_session: AsyncSession, username: str):
    result = await db_session.execute(select(User).where(or_(User.username == username, User.email == username)))
    
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


async def delete_user_by_id(db_session: AsyncSession, user_id: int) -> bool:
    user = await db_session.get(User, id)
    if not user:
        return False

    await db_session.delete(user)
    await db_session.commit()

    return True


async def delete_all_users(db_session: Session):
    result = await db_session.execute(select(User))
    users = result.scalars().all()

    await db_session.delete(users)
    await db_session.commit()