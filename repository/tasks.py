from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Task
from app.schemas import STaskAdd, STaskUpdate


class TaskRepository:

    @classmethod
    async def get_task(
        cls,
        task_id: int,
        user_id: int,
        session: AsyncSession,
    ):

        stmt = select(Task).where(
            Task.id == task_id,
            Task.user_id == user_id,
        )

        result = await session.execute(stmt)

        return result.scalar_one_or_none()

    @classmethod
    async def get_tasks(
        cls,
        user_id: int,
        session: AsyncSession,
    ):

        stmt = select(Task).where(Task.user_id == user_id)

        result = await session.execute(stmt)

        return result.scalars().all()

    @classmethod
    async def create_task(
        cls,
        data: STaskAdd,
        user_id: int,
        session: AsyncSession,
    ):

        task = Task(
            **data.model_dump(),
            user_id=user_id,
        )

        session.add(task)

        await session.commit()
        await session.refresh(task)

        return task

    @classmethod
    async def update_task(
        cls,
        task_id: int,
        user_id: int,
        data: STaskUpdate,
        session: AsyncSession,
    ):

        task = await cls.get_task(
            task_id,
            user_id,
            session,
        )

        if not task:
            return None

        update_data = data.model_dump(exclude_unset=True)

        for k, v in update_data.items():
            setattr(task, k, v)

        await session.commit()
        await session.refresh(task)

        return task

    @classmethod
    async def delete_task(
        cls,
        task_id: int,
        user_id: int,
        session: AsyncSession,
    ):

        task = await cls.get_task(
            task_id,
            user_id,
            session,
        )

        if not task:
            return None

        await session.delete(task)
        await session.commit()

        return task