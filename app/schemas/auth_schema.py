from pydantic import BaseModel,EmailStr,Field,ConfigDict,field_validator
from app.models import UserRole


# user base schema

class UserBase(BaseModel):
    full_name:str=Field(...,min_length=3,max_length=100)
    email:EmailStr

    @field_validator("full_name")
    @classmethod
    def validate_name(cls,value):
        if not value.strip():
            raise ValueError("full name cannot be empty")
        return value.title()


# register schema

class UserRegister(UserBase):
    password:str=Field(...,min_length=6,max_length=100)


# login schema

class UserLogin(BaseModel):
    email:EmailStr
    password:str


# user response schema

class UserResponse(UserBase):
    id:int
    role:UserRole
    is_active:bool

    model_config=ConfigDict(from_attributes=True)


# token schema

class Token(BaseModel):
    access_token:str
    token_type:str


# token data schema

class TokenData(BaseModel):
    email:str|None=None