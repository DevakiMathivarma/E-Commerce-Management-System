from datetime import datetime,timedelta,timezone
from jose import jwt,JWTError
from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.config import settings
from app.db import get_db
from app.models import User,UserRole
from app.schemas.auth_schema import TokenData


# oauth2 configuration

oauth2_scheme=OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


# create jwt access token

def create_access_token(data:dict):
    to_encode=data.copy()
    expire=datetime.now(timezone.utc)+timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    return jwt.encode(to_encode,settings.SECRET_KEY,algorithm=settings.ALGORITHM)


# get current user

def get_current_user(token:str=Depends(oauth2_scheme),db:Session=Depends(get_db)):
    credentials_exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="could not validate credentials",headers={"WWW-Authenticate":"Bearer"})
    try:
        payload=jwt.decode(token,settings.SECRET_KEY,algorithms=[settings.ALGORITHM])
        email=payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data=TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user=db.query(User).filter(User.email==token_data.email).first()
    if user is None:
        raise credentials_exception
    return user


# admin authorization

def admin_required(current_user:User=Depends(get_current_user)):
    if current_user.role!=UserRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="admin access required")
    return current_user


# customer authorization

def customer_required(current_user:User=Depends(get_current_user)):
    if current_user.role!=UserRole.CUSTOMER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="customer access required")
    return current_user