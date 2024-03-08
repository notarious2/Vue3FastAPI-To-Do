from fastapi import APIRouter, Depends, HTTPException, status
from database import get_async_session
import schemas, crud
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from schemas import UserDisplay, UserCreate


router = APIRouter(
    prefix = '/users',
    tags = ['user']
)

#CREATE A USER
@router.post("/register/", response_model=UserDisplay)
async def add_user(user_schema: UserCreate, db_session: AsyncSession = Depends(get_async_session)):

    user = await crud.get_user_by_username(db_session, user_schema.username)
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
        detail="Username already exists")
    
    # checking if email already exists 
    user = await crud.get_user_by_email(db_session, user_schema.email)
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
        detail="Email already exists")
    
    return await crud.create_user(db_session, user_schema)
    

@router.get("/", response_model=List[UserDisplay])
async def get_users(db_session: AsyncSession = Depends(get_async_session)):
    users = await crud.get_users(db_session)
    return users


@router.delete("/{user_id}/")
async def delete_user_by_id(user_id: int, db_session: AsyncSession = Depends(get_async_session)):
    return await crud.delete_user_by_id(db_session, user_id)


@router.delete("/")
async def delete_all_users(db_session: AsyncSession = Depends(get_async_session)):
    return await crud.delete_all_users(db_session)