from fastapi import APIRouter, Depends, HTTPException, status

from app.authh.dependencies import get_current_user
from app.database import SessionDep
from app.models import User
from app.repository.tasks import TaskRepository
from app.schemas import STask, STaskAdd, STaskUpdate


router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
)


@router.get("", response_model=list[STask])
async def get_tasks(
    session: SessionDep,
    user: User = Depends(get_current_user),
):

    return await TaskRepository.get_tasks(
        user.id,
        session,
    )


@router.get("/{task_id}", response_model=STask)
async def get_task(
    task_id: int,
    session: SessionDep,
    user: User = Depends(get_current_user),
):

    task = await TaskRepository.get_task(
        task_id,
        user.id,
        session,
    )

    if not task:
        raise HTTPException(404, "Not found")

    return task


@router.post(
    "",
    response_model=STask,
    status_code=status.HTTP_201_CREATED,
)
async def create_task(
    data: STaskAdd,
    session: SessionDep,
    user: User = Depends(get_current_user),
):

    return await TaskRepository.create_task(
        data,
        user.id,
        session,
    )


@router.put("/{task_id}", response_model=STask)
async def update_task(
    task_id: int,
    data: STaskUpdate,
    session: SessionDep,
    user: User = Depends(get_current_user),
):

    task = await TaskRepository.update_task(
        task_id,
        user.id,
        data,
        session,
    )

    if not task:
        raise HTTPException(404, "Not found")

    return task


@router.delete("/{task_id}", status_code=204)
async def delete_task(
    task_id: int,
    session: SessionDep,
    user: User = Depends(get_current_user),
):

    task = await TaskRepository.delete_task(
        task_id,
        user.id,
        session,
    )

    if not task:
        raise HTTPException(404, "Not found")