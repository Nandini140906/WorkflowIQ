#get user info
from fastapi import APIRouter,HTTPException,Depends,status
from sqlalchemy.orm import Session
from database import get_db
import schemas
import crud

router=APIRouter()
@router.get("/user/{user_id}",response_model=schemas.UserResponse)
def get_user(user_id:int,db:Session=Depends(get_db)):
    #Get user ID
    user=crud.get_user_id(db,user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User Not Found" 
        )
    return user
