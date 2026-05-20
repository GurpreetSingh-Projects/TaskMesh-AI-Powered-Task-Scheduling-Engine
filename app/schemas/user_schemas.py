from pydantic import BaseModel, EmailStr, Field, ConfigDict,  model_validator

class UserCreate(BaseModel):
    email: EmailStr
    password: str= Field(min_length=8, max_length=25)
    
    model_config=ConfigDict(extra="forbid")
    
class UserPublic(BaseModel):
    email: EmailStr
    user_id: int

class UserLogin(UserCreate):
    pass
    
class UserLoginResponse(BaseModel):
    access_token: str
    type: str
    user: UserPublic
    
class UserRead(BaseModel):
    user_id: int
    email: EmailStr
    
    model_config= ConfigDict(from_attributes= True)
    