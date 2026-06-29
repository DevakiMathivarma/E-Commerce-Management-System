from fastapi import APIRouter,Depends,status
from sqlalchemy.orm import Session

from app.db import get_db
from app.schemas.auth_schema import UserRegister,UserLogin,UserResponse,Token
from app.services.auth_service import register_user_service,login_user_service


# auth router

router=APIRouter(prefix="/auth",tags=["Authentication"])


# register api

@router.post("/register",response_model=UserResponse,status_code=status.HTTP_201_CREATED)
def register(user:UserRegister,db:Session=Depends(get_db)):
    return register_user_service(user,db)


# login api

@router.post("/login",response_model=Token)
def login(user:UserLogin,db:Session=Depends(get_db)):
    return login_user_service(user,db)