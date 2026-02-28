from fastapi import APIRouter,Depends,HTTPException,status,Query
from sqlalchemy.orm import Session
from database import get_db
from typing import List
import schemas
import crud
from ml_model import predict_priority

router=APIRouter()

@router.post("/tasks",response_model=schemas.TaskResponse,status_code=status.HTTP_201_CREATED)
def create_task(task:schemas.TaskCreate,user_id:int=Query(...),db:Session=Depends(get_db)):
    #creates new task with ML predicted priority
    predicted_priority=predict_priority(title=task.title,deadline=task.deadline,category=task.category)
    #creates task with predicted priority
    new_task=crud.create_task(db,task,user_id,priority=predicted_priority)

    return new_task

@router.get("/tasks",response_model=List[schemas.TaskResponse])
def get_tasks(user_id:int=Query(...),skip:int=0,limit:int=100,db:Session=Depends(get_db)):
    #Get all tasks by user
    tasks=crud.get_tasks(db,user_id,skip,limit)
    return tasks

@router.get("/tasks/{task_id}",response_model=schemas.TaskResponse)
def get_task(task_id:int,user_id:int=Query(...),db:Session=Depends(get_db)):
    #Get tasks by specific ID
    task=crud.get_task(db,task_id,user_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return task

@router.put("/tasks/{task_id}",response_model=schemas.TaskResponse)
def update_task(task_id:int,task_update:schemas.TaskUpdate,user_id:int=Query(...),db:Session=Depends(get_db)):
    #update tasks
    updated_task=crud.update_task(db,task_id,user_id,task_update)

    if not updated_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task Not Found"
        )
    return updated_task

@router.delete("/tasks/{task_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id:int,user_id:int=Query(...),db:Session=Depends(get_db)):
    #Delete Task
    deleted_task=crud.delete_task(db,user_id,task_id)
    if not deleted_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task Not Found"
        )
    return None

