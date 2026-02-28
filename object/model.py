#Define the structure of database tables
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Float,Integer,String, Text,DateTime,ForeignKey
from database import Base
from datetime import datetime

class User(Base):
#stores user accounts
    __tablename__="users"
    id=Column(Integer,primary_key=True,index=True)

    name=Column(String,nullable=False)

    email=Column(String,unique=True,index=True,nullable=False)

    password=Column(String,nullable=False)

    created_at=Column(DateTime,default=datetime.utcnow)


    tasks=relationship("Task",back_populates="owner",cascade="all,delete-orphan")
    workflows=relationship("Workflow",back_populates="owner",cascade="all,delete-orphan")

class Task(Base):
#stores indiviual task
    __tablename__="tasks"
    id=Column(Integer,primary_key=True,index=True)

    title=Column(String,nullable=False)

    description=Column(Text,nullable=True)#Optional

    category=Column(String,nullable=False)

    deadline=Column(DateTime,nullable=True)

    status=Column(String,default="pending")

    priority=Column(String,nullable=True)#decided by model

    created_at=Column(DateTime,default=datetime.utcnow)

#Foreign key to link task to user
    user_id=Column(Integer,ForeignKey("users.id"))
    workflow_id=Column(Integer,ForeignKey("workflows.id"))

#Relationship to User
    owner=relationship("User",back_populates="tasks")
    workflows=relationship("Workflow",back_populates="tasks")
    logs=relationship("ProductivityLog",back_populates="task",cascade="all,delete-orphan")

class Workflow(Base):
#store workflow info with multiple tasks
    __tablename__="workflows"
    id=Column(Integer,primary_key=True,index=True)

    name=Column(String,nullable=False)

    description=Column(Text,nullable=True)

    created_at=Column(DateTime,default=datetime.utcnow)

#Foreign key to link workflow to user
    user_id=Column(Integer,ForeignKey("users.id"))

#Relationship to User
    owner=relationship("User",back_populates="workflows")
    tasks=relationship("Task",back_populates="workflows",cascade="all,delete-orphan")

class ProductivityLog(Base):
#store productivity logs for tasks
    __tablename__="productivity_logs"
    id=Column(Integer,primary_key=True,index=True)

    created_at=Column(DateTime,default=datetime.utcnow,nullable=False)

    
    hours_spent = Column(Float, nullable=False)
    notes = Column(Text, nullable=True)   # also missing entirely
    date = Column(String, nullable=True)    


#Foreign key to link log to task
    task_id=Column(Integer,ForeignKey("tasks.id"))  
#Relationship to Task
    task=relationship("Task",back_populates="logs")