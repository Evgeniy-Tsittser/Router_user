from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.backend.db_depends import get_db
from typing import Annotated
from app.models import Task, User
from app.schemas import CreateTask, UpdateTask
from sqlalchemy import insert, select, update, delete

task_router = APIRouter(prefix="/task", tags=["task"])

#________________________________
@task_router.get("/")
async def get_all_users(db: Annotated[Session, Depends(get_db)]):
    tasks = db.scalars(select(Task)).all()
    return tasks

#_____________________________________
@task_router.get("/task_id/{task_id}")
async def task_by_id(task_id: int, db: Annotated[Session, Depends(get_db)]):
    task = db.execute(select(Task).where(Task.id == task_id)).scalars().one_or_none()
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Task not found'
        )
    return task

#__________________________________
@task_router.post("/create")
async def create_task(create_task_model: CreateTask, db: Annotated[Session, Depends(get_db)], user_id: int):
    user = db.execute(select(User).where(User.id == user_id)).scalars().one_or_none()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User was not found'
        )
    db.execute(insert(Task).values(title=create_task_model.title,
                       content=create_task_model.content,
                       priority=create_task_model.priority,
                       user_id=user_id)
               )
    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Task create is successful!'
    }

#____________________________________
@task_router.put("/update/{task_id}")
async def update_task(create_task_model: UpdateTask, task_id: int, db: Annotated[Session, Depends(get_db)]):
    task = db.execute(select(Task).where(Task.id == task_id)).scalars().one_or_none()
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Task was not found'
        )
    db.execute(update(Task).where(Task.id == task_id)
               .values(title=create_task_model.title,
                       content=create_task_model.content,
                       priority=create_task_model.priority)
               )
    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Task update is successful!'
    }

#______________________________________
@task_router.delete("/delete/{task_id}")
async def delete_task(task_id: int, db: Annotated[Session, Depends(get_db)]):
    task = db.execute(select(Task).where(Task.id == task_id)).scalars().one_or_none()
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Task was not found'
        )
    db.execute(delete(Task).where(Task.id == task_id))

    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Task delete is successful!'
    }