#handles user sign up and login
from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from database import get_db
import crud
import schemas
from auth import verify_password,create_access_token #create JWT token

router=APIRouter()
@router.post("/signup",response_model=schemas.UserResponse,status_code=status.HTTP_201_CREATED)
def signup(user:schemas.UserCreate,db:Session=Depends(get_db)):
    existing_user=crud.get_user_email(db,user.email)
    #search database for user with this email,returns user object if found

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registred"
        )
    new_user=crud.create_user(db,user)
    return new_user


#Login Endpoint
@router.post("/login",response_model=schemas.Token)
def login(user:schemas.UserLogin,db:Session=Depends(get_db)):
    db_user=crud.get_user_email(db,user.email)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Credentials"
        )
    if not verify_password(user.password,db_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="UNAUTHORISED CREDENTIALS"
        )
    
    access_token=create_access_token(data={"user_id":db_user.id,"email":db_user.email})
    return{"access_token":access_token,"token_type":"bearer",
           "user_id":db_user.id,"name":db_user.name}

    