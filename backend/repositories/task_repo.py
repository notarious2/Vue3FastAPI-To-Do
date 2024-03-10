from datetime import date

from fastapi import HTTPException, status
from sqlalchemy import and_, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from models import Task, User
from schemas import CreateTaskSchema, UpdateTaskSchema


class TaskRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_task_by_id(self, task_id: int) -> Task | None:
        task = await self.db_session.get(Task, task_id)
        return task

    async def get_tasks_by_date(self, selected_date: date, current_user: User) -> list[Task]:
        statement = (
            select(Task)
            .where(and_(Task.posted_at == selected_date, Task.user_id == current_user.id))
            .order_by(Task.priority.asc())
        )
        result = await self.db_session.execute(statement)
        tasks = result.scalars().all()
        return tasks

    async def create_task(self, create_task_schema: CreateTaskSchema, current_user: User) -> Task:
        task = Task(
            priority=create_task_schema.priority,
            text=create_task_schema.text,
            user_id=current_user.id,
            posted_at=create_task_schema.posted_at,
        )

        self.db_session.add(task)
        await self.db_session.commit()
        await self.db_session.refresh(task)
        return task

    async def delete_task(self, task_id: int, user_id: int) -> bool:
        result = await self.db_session.execute(select(Task).where(and_(Task.id == task_id, Task.user_id == user_id)))
        task = result.scalar_one_or_none()
        if not task:
            return False

        await self.db_session.delete(task)
        await self.db_session.commit()
        return True

    async def update_task(self, task: Task, new_task: UpdateTaskSchema) -> Task:
        if new_task.text:
            task.text = new_task.text
        if new_task.priority:
            task.priority = new_task.priority
        if new_task.completed is not None:
            task.completed = new_task.completed

        await self.db_session.commit()
        await self.db_session.refresh(task)

        return task

    async def bulk_update_priorities(self, priorities: dict[int, int], current_user: User):
        """
        priorities hold id:new_priority key-pair dictonary
        """
        # make sure all tasks (ids) belong to the current user
        result = await self.db_session.execute(
            select(Task.id).where(and_(Task.user_id == current_user.id, Task.id.in_(priorities))),
        )
        task_ids = result.scalars().all()  # returns list of ids

        # task ids provided doesn't match task ids found for user
        if not len(priorities) == len(task_ids):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Provided ids doesn't match tasks of the user [{priorities}]",
            )

        # unpack into {id: key, priority:value} list
        priorities_to_update = [{"id": task_id, "priority": priority} for task_id, priority in priorities.items()]

        await self.db_session.execute(update(Task), priorities_to_update)
        await self.db_session.commit()
