from datetime import date

from auth import get_current_user
from database import get_async_session
from fastapi import APIRouter, Depends, HTTPException, Response, status
from models import User
from repositories.task_repo import TaskRepository
from schemas import (
    CreateTaskSchema,
    DisplayTaskSchema,
    UpdateTaskPrioritiesSchema,
    UpdateTaskSchema,
)
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/task", tags=["task"])


@router.post("/", response_model=DisplayTaskSchema)
async def add_task(
    create_task_schema: CreateTaskSchema,
    db_session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
):
    task_repo = TaskRepository(db_session)
    task = await task_repo.create_task(create_task_schema, current_user)
    return task


@router.get("/", response_model=list[DisplayTaskSchema])
async def get_tasks(
    selected_date: date,
    db_session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
):
    task_repo = TaskRepository(db_session)
    tasks = await task_repo.get_tasks_by_date(selected_date, current_user)
    return tasks


@router.patch("/update-order/")
async def update_tasks_order(
    priorities_schema: UpdateTaskPrioritiesSchema,
    db_session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
):
    task_repo = TaskRepository(db_session)

    await task_repo.bulk_update_priorities(priorities_schema.priorities, current_user)

    return "Priorities have been updated"


@router.patch("/{task_id}/", response_model=DisplayTaskSchema)
async def update_task(
    task_id: int,
    update_task_schema: UpdateTaskSchema,
    db_session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
):
    task_repo = TaskRepository(db_session)
    task = await task_repo.get_task_by_id(task_id)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found",
        )

    if not task.user_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Task does not belong to the current user",
        )

    updated_task = await task_repo.update_task(task, new_task=update_task_schema)

    return updated_task


@router.delete("/{task_id}/")
async def delete_task_by_id(
    task_id: str,
    db_session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
):
    task_repo = TaskRepository(db_session)

    if not await task_repo.delete_task(task_id, current_user.id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"task with id {task_id} not found",
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)
