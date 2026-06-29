from sqlalchemy.orm import Session
from fastapi import HTTPException,status

from app.models import User,UserRole
from app.schemas.auth_schema import UserRegister,UserLogin,UserResponse,Token
from app.utils.hash import hash_password,verify_password
from app.utils.auth import create_access_token


# register service

def register_user_service(user:UserRegister,db:Session):

    existing_user=db.query(User).filter(User.email==user.email).first()

    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="email already registered")

    new_user=User(full_name=user.full_name,email=user.email,password=hash_password(user.password),role=UserRole.CUSTOMER)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# login service

def login_user_service(user:UserLogin,db:Session):

    db_user=db.query(User).filter(User.email==user.email).first()

    if not db_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="invalid email or password")

    if not verify_password(user.password,db_user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="invalid email or password")

    access_token=create_access_token({"sub":db_user.email})

    return {"access_token":access_token,"token_type":"bearer"}