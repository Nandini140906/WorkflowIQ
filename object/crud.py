#CRUD Operations
#CREATE,READ,UPDATE,DELETE

from sqlalchemy.orm import Session
import model
import schemas
from auth import hash_password
from typing import Optional,List

#USER  CRUD Operations
def get_user_email(db:Session,email:str):
    return db.query(model.User).filter(model.User.email==email).first()

def get_user_id(db:Session,user_id:int):
    return db.query(model.User).filter(model.User.id==user_id).first()

def create_user(db:Session,user:schemas.UserCreate):
    hashed_password=hash_password(user.password)
    #hashes the plain text and stores hashed ones
    

    db_user=model.User(
        name=user.name,
        email=user.email,
        password=hashed_password
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

#TASK CRUD Operations
def get_tasks(db:Session,user_id:int,skip:int=0,limit:int=100):
    return db.query(model.Task).filter(model.Task.user_id==user_id).offset(skip).limit(limit).all()
    
#to show limited number of tasks in a single web page
def get_task(db:Session,task_id:int,user_id:int):
    #get specific task
    return db.query(model.Task).filter(
        model.Task.id==task_id,
        model.Task.user_id==user_id).first()

def create_task(db:Session,task:schemas.TaskCreate,user_id:int,priority:str=None):
    #create a new task with ML predicted priority
    db_task=model.Task(
        **task.dict(),
        user_id=user_id,
        priority=priority
    )

    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def update_task(db:Session,task_id:int,user_id:int,task_update:schemas.TaskUpdate):
    #UPDATE tasks only required fields
    db_task=get_task(db,user_id,task_id)
    if not db_task:
        return None
    update_task=task_update.dict(exclude_unset=True)
    for key,value in update_task.items():
        setattr(db_task,key,value)

    db.commit()
    db.refresh(db_task)
    return db_task

def delete_task(db:Session,task_id:int,user_id:int):
    #delete task
    db_task=get_task(db,user_id,task_id)
    if not db_task:
        return None
    db.delete(db_task)
    db.commit()
    return db_task

#Workflow CRUD Operations    
def get_workflows(db:Session,user_id:int):
    #get all workflows for a user
    return db.query(model.workflows).filter(
        model.Workflow.user_id==user_id
    ).all()

def get_workflow(db:Session,user_id:int,workflow_id:int):
    #gets back specific workflow
    return db.query(model.workflows).filter(
        model.Workflow.id==workflow_id,
        model.Workflow.user_id==user_id
    ).first()

def create_workflow(db:Session,workflow:schemas.WorkflowCreate,user_id:int):
    #create new workflow
    db_workflow=model.Workflow(
        user_id=user_id,
        **workflow.dict()
         )
    db.add(db_workflow)
    db.commit()
    db.refresh(db_workflow)
    return db_workflow

def update_workflow(db:Session,workflow_update:schemas.WorkflowUpdate,user_id:int,workflow_id:int):
    db_update=get_workflow(db,workflow_id,user_id)
    if not db_update:
        return None
    
    update_data=update_workflow.dict(exclude_unset=True)
    for key,values in update_data.items():
        setattr(db_update,key,values)

    db.commit()
    db.refresh(db_update)
    return db_update

def delete_workflow(db:Session,workflow_id:int,user_id:int):
    #delete workflow
    db_workflow=get_workflow(db,workflow_id,user_id)
    if not db_workflow:
        return None
    
    db.delete(db_workflow)
    db.commit()
    return db_workflow()

#Productivity log CRUD Operations
def get_logs_by_task(db:Session,task_id:int,user_id:int):
    #get all logs for a task
    task=get_task(db,user_id,task_id)
    if not task:
        return []
    
    return db.query(model.ProductivityLog).filter(
        model.ProductivityLog.task_id==task_id).all()

def create_log(db:Session,log:schemas.ProductivityLogCreate,user_id:int):
    #create new productivity log
    task=get_task(db,log.task_id,user_id)
    if not task:
        return None
    
    db_log=model.ProductivityLog(**log.dict())
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log


def update_log(db:Session,user_id:int,log_id:int,log_update:schemas.ProductivityLogUpdate):
    db_log=db.query(model.ProductivityLog).filter(model.ProductivityLog.id==log_id).first()
    if not db_log:
        return None
    
    task=get_task(db,db_log.task_id,user_id)
    if not task:
        return None
    
    update_data=log_update.dict(exclude_unset=True)
    for key,value in update_data.items():
        setattr(db_log,key,value)

    db.commit()
    db.refresh(db_log)
    return db_log

def delete_log(db:Session,log_id:int,user_id:int):
    #Delete productivity log
    db_log=db.query(model.ProductivityLog).filter(model.ProductivityLog.id==log_id).first()

    if not db_log:
        return None
    task=get_task(db,db_log.task_id,user_id)
    if not task:
        return None
    
    db.delete(db_log)
    db.commit()
    return db_log