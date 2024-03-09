
from fastapi import APIRouter, Depends, HTTPException, status, Request, Response
import crud
from schemas import CreateTaskSchema, UpdateTaskSchema, DisplayTaskSchema, UpdateTaskPrioritiesSchema, TasksByDateSchema
from auth import get_current_user
from database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from models import User
from datetime import date

router = APIRouter(prefix = '/task', tags = ['task'])



@router.post("/", response_model=DisplayTaskSchema)
async def add_task(create_task_schema: CreateTaskSchema, db_session: AsyncSession = Depends(get_async_session), current_user: User = Depends(get_current_user)):
    task = await crud.create_task(db_session, create_task_schema, current_user)
    return task

@router.get("/", response_model=list[DisplayTaskSchema])
async def get_tasks(request: Request, selected_date: date, db_session: AsyncSession = Depends(get_async_session), current_user: User = Depends(get_current_user)):
    tasks =  await crud.get_tasks_by_date(db_session, selected_date, current_user)
    return tasks



# GET ALL TASKS OF A USER - BASED ON AUTHORIZATION
# @router.get("/", response_model=List[schemas.TaskDisplay])
# async def get_tasks(db: Session = Depends(get_db), current_user: models.UserModel = Depends(get_current_user)):
#     return crud.get_tasks(db=db, current_user=current_user)


@router.patch("/{task_id}/", response_model=DisplayTaskSchema)
async def update_task(task_id: int, update_task_schema: UpdateTaskSchema, db_session: AsyncSession = Depends(get_async_session), current_user: User = Depends(get_current_user)):
    task = await crud.get_task_by_id(db_session, task_id)

    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail = f"task with id {task_id} not found")

    if not task.user_id == current_user.id:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
        detail = "Task does not belong to the current user")
    

    updated_task =  await crud.update_task(db_session, task, new_task=update_task_schema)    
    
    return updated_task


@router.delete("/{task_id}/")
async def delete_task_by_id(task_id:str, db_session: AsyncSession = Depends(get_async_session), current_user: User = Depends(get_current_user)):
    await crud.delete_task(db_session, task_id, current_user.id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.patch("/update/order/")
async def update_tasks_order(priorities_schema: UpdateTaskPrioritiesSchema, db_session: AsyncSession = Depends(get_async_session), current_user: User = Depends(get_current_user)):
    
    await crud.bulk_update_priorities(db_session, priorities_schema.priorities, current_user)

    return "Priorities have been updated" 
