from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm.session import Session
from database import get_db
import schemas, crud
from typing import List

#CREATING A ROUTER FOR USER
router = APIRouter(
    prefix = '/user',
    tags = ['user']
)

#CREATE A USER
@router.post("/register/", response_model=schemas.UserDisplay)
async def add_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # checking if username already exists 
    user_exists = crud.get_user_by_username(db=db, username=user.username)
    if user_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
        detail="Username already exists")
    # checking if email already exists 
    email_exists = crud.get_user_by_email(db=db, email=user.email)
    if email_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
        detail="Email already exists")
    return crud.add_user(user=user, db=db)
    
# GET ALL USERS
@router.get("", response_model=List[schemas.UserDisplay])
async def get_users(db: Session = Depends(get_db)):
    return crud.get_users(db=db)

# DELETE USER BY ID
@router.get("/delete/{user_id}")
async def delete_user_by_id(user_id: str, db: Session = Depends(get_db)):
    return crud.delete_user_by_id(user_id=user_id, db=db)

# DELETE ALL USERS
@router.get("/delete")
async def delete_all_users(db: Session = Depends(get_db)):
    return crud.delete_all_users(db=db)