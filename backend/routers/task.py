
from fastapi import APIRouter, Depends
from sqlalchemy.orm.session import Session
from database import get_db
import schemas, crud, models
from typing import List
from auth import get_current_user #to get authorized user

#CREATING A ROUTER FOR USER
router = APIRouter(
    prefix = '/task',
    tags = ['task']
)



# CREATE A TASK
@router.post("/")
async def add_task(task: schemas.TaskCreate, db: Session = Depends(get_db), current_user: models.UserModel = Depends(get_current_user)):
    crud.add_task(task=task, db=db, current_user=current_user)
    return "OK"
# GET ALL TASKS OF A USER - BASED ON AUTHORIZATION
@router.get("/", response_model=List[schemas.TaskDisplay])
async def get_tasks(db: Session = Depends(get_db), current_user: models.UserModel = Depends(get_current_user)):
    return crud.get_tasks(db=db, current_user=current_user)


# UPDATE ANY PASSED FIELD OF THE TASK FOR LOGGED IN USER
@router.patch("/{task_id}")
async def update_task(task_id: str, task: schemas.TaskOptional, db: Session = Depends(get_db), current_user: models.UserModel = Depends(get_current_user)):
    return crud.update_task(db=db, task_id=task_id, new_task=task, user_id=current_user.user_id)    


# DELETE TASK BY ID
@router.delete("/{task_id}")
async def delete_task_by_id(task_id:str, db: Session = Depends(get_db), current_user: models.UserModel = Depends(get_current_user)):
    return crud.delete_task_by_id(task_id=task_id, db=db, user_id=current_user.user_id)


@router.patch("/update/order")
async def update_tasks_order(payload: dict, db: Session = Depends(get_db), current_user: models.UserModel = Depends(get_current_user)):
    return crud.update_task_order(db=db, payload=payload, current_user=current_user)    

# GET ALL TASKS OF ALL USERS
@router.get("/all", response_model=List[schemas.TaskDisplay])
async def get__all_tasks(db: Session = Depends(get_db)):
    return crud.get_all_tasks(db=db)

# DELETE ALL TASKS IRRESPECTIVE FOR ALL USERS
@router.get("/all/delete")
async def delete_all_tasks(db: Session = Depends(get_db)):
    return crud.delete_all_tasks(db=db)