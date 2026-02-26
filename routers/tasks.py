from fastapi import APIRouter, HTTPException, status

from app.database import SessionDep
from app.repository.tasks import TaskRepository
from app.schemas import STask, STaskAdd, STaskUpdate


router = APIRouter(prefix="/tasks", tags=["for tasks"])


@router.get("/{task_id}", response_model=STask)
async def get_task(task_id: int, session: SessionDep):

    task = await TaskRepository.get_task(task_id, session)

    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")

    return task


@router.get("", response_model=list[STask])
async def get_tasks(session: SessionDep):

    return await TaskRepository.get_tasks(session)


@router.post("", response_model=STask, status_code=status.HTTP_201_CREATED)
async def create_task(
    task: STaskAdd,
    user_id: int,
    session: SessionDep,
):

    new_task = await TaskRepository.add_task(task, user_id, session)

    return new_task


@router.put("/{task_id}", response_model=STask)
async def update_task(
    task_id: int,
    task_data: STaskUpdate,
    session: SessionDep,
):

    updated_task = await TaskRepository.update_task(
        task_id,
        task_data,
        session,
    )

    if not updated_task:
        raise HTTPException(status_code=404, detail="Задача не найдена")

    return updated_task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: int, session: SessionDep):

    deleted_task = await TaskRepository.delete_task(task_id, session)

    if not deleted_task:
        raise HTTPException(status_code=404, detail="Задача не найдена")

    return None
