from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from repositories.user_repo import UserRepository
from schemas import UserCreate, UserDisplay

router = APIRouter(prefix="/users", tags=["user"])


@router.post("/register/", response_model=UserDisplay)
async def add_user(user_schema: UserCreate, db_session: AsyncSession = Depends(get_async_session)):
    user_repo = UserRepository(db_session)

    user = await user_repo.get_user_by_username(user_schema.username)
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already exists")

    # checking if email already exists
    user = await user_repo.get_user_by_email(user_schema.email)
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists")

    return await user_repo.create_user(user_schema)


@router.delete("/{user_id}/")
async def delete_user_by_id(user_id: int, db_session: AsyncSession = Depends(get_async_session)):
    user_repo = UserRepository(db_session)

    if not await user_repo.delete_user_by_id(user_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} is not found",
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)
