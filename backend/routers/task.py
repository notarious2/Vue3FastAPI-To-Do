
from fastapi import APIRouter, Depends
import schemas, crud, models
from schemas import CreateTaskSchema
from typing import List
from auth import get_current_user
from database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from models import User

router = APIRouter(
    prefix = '/task',
    tags = ['task']
)



# CREATE A TASK
@router.post("/")
async def add_task(create_task_schema: CreateTaskSchema, db_session: AsyncSession = Depends(get_async_session), current_user: User = Depends(get_current_user)):
    crud.add_task(db_session, create_task_schema, current_user)
    return "OK"


# # GET ALL TASKS OF A USER - BASED ON AUTHORIZATION
# @router.get("/", response_model=List[schemas.TaskDisplay])
# async def get_tasks(db: Session = Depends(get_db), current_user: models.UserModel = Depends(get_current_user)):
#     return crud.get_tasks(db=db, current_user=current_user)


# UPDATE ANY PASSED FIELD OF THE TASK FOR LOGGED IN USER
@router.patch("/{task_id}")
async def update_task(task_id: str, task: schemas.TaskOptional, db_session: AsyncSession = Depends(get_async_session), current_user: User = Depends(get_current_user)):
    return crud.update_task(db=db, task_id=task_id, new_task=task, user_id=current_user.user_id)    


# DELETE TASK BY ID
@router.delete("/{task_id}")
async def delete_task_by_id(task_id:str, db_session: AsyncSession = Depends(get_async_session), current_user: User = Depends(get_current_user)):
    return crud.delete_task(db_session, task_id, current_user.user_id)


@router.patch("/update/order")
async def update_tasks_order(payload: dict, db_session: AsyncSession = Depends(get_async_session), current_user: User = Depends(get_current_user)):
    return crud.update_task_order(db=db, payload=payload, current_user=current_user)    
