from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.backend.db_depends import get_db
from typing import Annotated
from app.models import User, Task
from app.schemas import CreateUser, UpdateUser
from sqlalchemy import insert, select, update, delete

user_router = APIRouter(prefix="/users", tags=["users"])


@user_router.get("/")
async def get_all_users(db: Annotated[Session, Depends(get_db)]):
    users = db.scalars(select(User)).all()
    return users


# ____________________________________
@user_router.get("/user_id/{user_id}")
async def user_by_id(user_id: int, db: Annotated[Session, Depends(get_db)]):
    user = db.execute(select(User).where(User.id == user_id)).scalars().one_or_none()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found'
        )
    return user


# ________________________________
@user_router.post("/create")
async def create_user(create_user_model: CreateUser, db: Annotated[Session, Depends(get_db)]):
    verify_user = db.execute(select(User).where(User.username == create_user_model.username)).scalars().one_or_none()
    if verify_user is not None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User with name username exist'
        )
    db.execute(insert(User).values(username=create_user_model.username,
                                   firstname=create_user_model.firstname,
                                   lastname=create_user_model.lastname,
                                   age=create_user_model.age))
    db.commit()
    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Successful'
    }


# ________________________________
@user_router.put("/update/{user_id}")
async def update_user(user_id: int, update_user_model: UpdateUser, db: Annotated[Session, Depends(get_db)]):
    user_update = db.execute(select(User).where(User.id == user_id)).scalars().one_or_none()
    if user_update is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User was not found'
        )
    db.execute(update(User).where(User.id == user_id)
               .values(username=update_user_model.username,
                       firstname=update_user_model.firstname,
                       lastname=update_user_model.lastname,
                       age=update_user_model.age)
               )
    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'User update is successful!'
    }


# ___________________________________
@user_router.get("/{user_id}/tasks")
async def tasks_by_user_id(user_id: int, db: Annotated[Session, Depends(get_db)]):
    user = db.execute(select(User).where(User.id == user_id)).scalars().one_or_none()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User was not found'
        )
    user_tasks = db.execute(select(Task).where(Task.user_id == user_id)).scalars().all()
    return user_tasks


# ______________________________________
@user_router.delete('/delete/{user_id}')
async def delete_user(user_id: int, db: Annotated[Session, Depends(get_db)]):
    user_delete = db.execute(select(User).where(User.id == user_id)).scalars().one_or_none()
    if user_delete is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User was not found'
        )
    db.execute(delete(Task).where(Task.user_id == user_id))
    db.delete(user_delete)
    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'User delete is successful!'
    }
