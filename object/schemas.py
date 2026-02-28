from __future__ import annotations  
from pydantic import BaseModel,EmailStr,Field
from typing import Optional,List
from datetime import datetime,date

#user schemas
class UserBase(BaseModel):
    name:str=Field(...,min_length=1,max_length=50)
    email:EmailStr

class UserCreate(UserBase):#this will inherit class UserBase
#new sign up for user
    password:str=Field(...,min_length=8)

class UserLogin(BaseModel):
    email:EmailStr
    password:str

class UserResponse(UserBase):
    id:int
    created_at:datetime

    class Config:
        from_attributes=True


# class TaskResponse:
#     pass
# class WorkflowResponse:
#     pass

class Tasks(UserResponse):
    tasks:List["TaskResponse"]=[]
    workflow:List['WorkflowResponse']=[]


#Task Schemas
class TaskBase(BaseModel):
    title:str=Field(...,min_length=1,max_length=25)
    category:str
    description:Optional[str]=None
    deadline:Optional[date]=None
    status:str=Field(default='pending')

class TaskCreate(BaseModel):
#Schema for creating a new task and user can optionally assign task to a workflow
    title: str
    category: str
    description:Optional[str]
    deadline: date
    status:str="pending"
    workflow_id:Optional[int]=None

class TaskUpdate(BaseModel):
#schema for updating tasks(all optional)
    title:Optional[str]=None
    description:Optional[str]=None
    category:Optional[str]=None
    deadline:Optional[date]=None
    priority:Optional[str]=None
    status:Optional[str]=None
    workflow_id:Optional[int]=None

class TaskResponse(TaskBase):
#schemas for returning task data
    id:int
    priority:Optional[str]=None
    workflow_id:Optional[int]=None
    created_at:datetime

    class Config:
        from_attributes=True
    #helps pydantic to connect with SQLAlchemy

class ProductivityLogResponse:
    pass



#workflow schemas
class WorkflowBase(BaseModel):
# Base schema with common workflow fields
    name:str=Field(...,min_length=2,max_length=50)
    description:Optional[str]=None

class WorkflowCreate(WorkflowBase):
    name:str
    description:Optional[str]=None
    steps:Optional[str]=None
#schema used to create a new workflow
#no need of additional fields,as we have directly inherited it to workflowBase

class WorkflowUpdate(BaseModel):
    name:Optional[str]=None
    description:Optional[str]=None

class WorkflowResponse(WorkflowBase):
#Schema for returning workflow data
    id:int
    created_at:datetime

    class Config:
        from_attributes=True

#Productivity Log schema
#used to track records of task and monitor how time is being used

class ProductivityLogBase(BaseModel):
    time_spent:float=Field(...,gt=0)
    #Base class with common log fields

class ProductivityLogCreate(ProductivityLogBase):
    task_id:int
    date:Optional[datetime]=None
    hours_spent: float = Field(..., gt=0)
    notes: Optional[str] = None
    
#if date not provided then the current date will be used

class ProductivityLogUpdate(BaseModel):
    time:Optional[float]=Field(None,gt=0)
    notes:Optional[str]=None
    date:Optional[str]=None

class ProductivityLogResponse(ProductivityLogBase):
#schemas for returning productivity log data
    id:int
    date:date
    created_at:datetime

    class Config:
        from_attributes=True

class PredictionRequest(BaseModel):
    #schema for prediction request
    title:str
    deadline:Optional[date]=None
    category:str
    #these are the features that ML model needs

class PredictionResponse(BaseModel):
    #schema for ML predcition response
    priority:str
    confidence:Optional[float]=None
    #Optionally return confidence score

#Authentication schema
class Token(BaseModel):
    #schema for JWT token response
    access_token:str
    token_type:str='bearer'

class TokenData(BaseModel):
    #schema for decoded token data
    user_id:Optional[int]=None
    email:Optional[str]=None



    

