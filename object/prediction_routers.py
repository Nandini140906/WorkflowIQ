#ML Prediction Route
from fastapi import APIRouter
import schemas
from ml_model import predict_priority as ml_predict #renaming it here

router=APIRouter()
@router.post("/predict-priority",response_model=schemas.PredictionResponse)
def predict_task_priority(request:schemas.PredictionRequest):#no database needed just ml prediction
    #predict task priority using ml
    priority=ml_predict(request.title,request.category,request.deadline)

    return{
        "priority":priority,
        "confidence":None
    }