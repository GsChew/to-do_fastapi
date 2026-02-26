from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Task
from app.schemas import STaskAdd, STaskUpdate


class TaskRepository:

    @classmethod
    async def get_task(cls, task_id: int, session: AsyncSession):
        query = select(Task).where(Task.id == task_id)

        result = await session.execute(query)

        return result.scalar_one_or_none()

    @classmethod
    async def get_tasks(cls, session: AsyncSession):
        query = select(Task)

        result = await session.execute(query)

        return result.scalars().all()

    @classmethod
    async def add_task(
        cls,
        data: STaskAdd,
        user_id: int,
        session: AsyncSession
    ):
        task_dict = data.model_dump()

        task = Task(**task_dict, user_id=user_id)

        session.add(task)

        await session.commit()
        await session.refresh(task)

        return task

    @classmethod
    async def delete_task(cls, task_id: int, session: AsyncSession):
        query = select(Task).where(Task.id == task_id)

        result = await session.execute(query)

        task = result.scalar_one_or_none()

        if not task:
            return None

        await session.delete(task)
        await session.commit()

        return task

    @classmethod
    async def update_task(
        cls,
        task_id: int,
        data: STaskUpdate,
        session: AsyncSession
    ):
        query = select(Task).where(Task.id == task_id)

        result = await session.execute(query)

        task = result.scalar_one_or_none()

        if not task:
            return None

        update_data = data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(task, field, value)

        await session.commit()
        await session.refresh(task)

        return task
