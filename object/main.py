from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine,Base
from fastapi import APIRouter
import auth_routers,log_routers,prediction_routers,tasks_routers,users_routers,workflow_routers

Base.metadata.create_all(bind=engine)

app=FastAPI(
    title="WorkflowIQ",
    description="AI powered workflow tracking system",
    version="1.0.0"
)

app.add_middleware(CORSMiddleware,
                   allow_origins=["*"],
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"],
                   )


# Include all routers
app.include_router(auth_routers.router, prefix="/api", tags=["Authentication"])
app.include_router(users_routers.router, prefix="/api", tags=["Users"])
app.include_router(tasks_routers.router, prefix="/api", tags=["Tasks"])
app.include_router(workflow_routers.router, prefix="/api", tags=["Workflows"])
app.include_router(log_routers.router, prefix="/api", tags=["Productivity Logs"])
app.include_router(prediction_routers.router, prefix="/api", tags=["ML Prediction"])

@app.get("/")
def root():
    return{
        "message":"Welcome to WorkflowIQ API",
        "status":"success",
        "version":"1.0.0"
    }

@app.get("/health")
def health_check():
    return{
        "status": "healthy",
        "database": "connected"
    }