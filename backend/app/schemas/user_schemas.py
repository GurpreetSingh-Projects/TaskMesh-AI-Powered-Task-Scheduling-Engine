from pydantic import BaseModel, EmailStr, Field, ConfigDict
from uuid import UUID
from ..models.user_roles import UserRoles

class UserCreate(BaseModel):
    email: EmailStr
    password: str= Field(min_length=8, max_length=25)
        
    model_config=ConfigDict(extra="forbid")
    
class UserPublic(BaseModel):
    email: EmailStr
    user_id: UUID
    role: UserRoles
    
    model_config = ConfigDict(from_attributes= True)
    
class UserLogin(BaseModel):
    email: EmailStr
    password: str= Field(min_length=8, max_length=256)
    
class UserLoginResponse(BaseModel):
    access_token: str
    type: str
    user: UserPublic
    
class UserRead(BaseModel):
    user_id: UUID
    email: EmailStr
    role: UserRoles
        
    model_config= ConfigDict(from_attributes= True)

class GetAllUsersResponse(BaseModel):
    items: list[UserRead]
    total: int
    page: int
    page_size: int
    total_pages: int