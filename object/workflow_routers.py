from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
import schemas
import crud

router=APIRouter()
@router.post("/workflows",response_model=schemas.WorkflowResponse,status_code=status.HTTP_201_CREATED)
def create_workflow(workflow:schemas.WorkflowCreate,user_id:int,workflow_id:int,db:Session=Depends(get_db)):
    #create new workflow
    new_workflow=crud.create_workflow(db,workflow,user_id)
    return new_workflow

@router.get("/workflows",response_model=List[schemas.WorkflowResponse])
def get_workflows(user_id:int,db:Session=Depends(get_db)):
    #Get all workflows for a user
    workflows=crud.get_workflows(db,user_id)
    return workflows

@router.get("/workflows/{workflow_id}",response_model=schemas.WorkflowResponse)
def get_workflow(workflow_id:int,user_id:int,db:Session=Depends(get_db)):
    #get specific workflows
    workflow=crud.get_workflow(db,user_id,workflow_id)
    if not workflow:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workflow not found"
        )
    return workflow

@router.put("/workflows/{workflow_id}",response_model=List[schemas.WorkflowResponse])
def update_workflow(workflow_update:schemas.WorkflowUpdate,user_id:int,workflow_id:int,db:Session=Depends(get_db)):
    #update all workflows
    updated_workflows=crud.update_workflow(db,user_id,workflow_id,workflow_update)
    if not updated_workflows:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workflow not found"
        )
    return updated_workflows

@router.delete("/workflows/{workflow_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_workflow(workflow_id:int,user_id:int,db:Session=Depends(get_db)):
    deleted_workflow=crud.delete_workflow(db,user_id,workflow_id)

    if not deleted_workflow:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="NOT FOUND"
        )
    return None
