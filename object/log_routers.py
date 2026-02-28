#Productivity Log Routes
#CRUD Operations for productivity log

from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from database import get_db
from typing import List
import schemas
import crud

router=APIRouter()

@router.post("/logs",response_model=schemas.ProductivityLogResponse,status_code=status.HTTP_201_CREATED)
def create_log(log:schemas.ProductivityLogCreate,user_id:int,db:Session=Depends(get_db)):
    #Create new productivity log
    new_log=crud.create_log(db,log,user_id)
    if not new_log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="NOT FOUND"
        )
    return new_log

@router.get("/logs/task/{task_id}",response_model=List[schemas.ProductivityLogResponse])
def get_logs_by_tasks(task_id:int,user_id:int,db:Session=Depends(get_db)):
    #Get all logs for a specific task
    logs=crud.get_logs_by_task(db,task_id,user_id)
    return logs

@router.put("/logs/{log_id}",response_model=schemas.ProductivityLogResponse)
def update_log(log_id:int,user_id:int,log_update:schemas.ProductivityLogUpdate,db:Session=Depends(get_db)):
    updated_log=crud.update_log(db,user_id,log_id,log_update)
    if not update_log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="NOT FOUND"
        )
    return updated_log

@router.delete("/logs/{log_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_log(log_id:int,user_id:int,db:Session=Depends(get_db)):
    #Delete Productivity Log
    delete_log=crud.delete_log(db,log_id,user_id)
    if not delete_log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not Found"
        )
    return None
