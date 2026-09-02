from pydantic import BaseModel
from pydantic import EmailStr
from uuid import UUID
from datetime import datetime

class UserCreateRequestSchema(BaseModel):
    email: EmailStr
    password: str
    image_url: str | None = None

class UserLoginRequestSchema(BaseModel):
    email: EmailStr
    password: str

class UserReadResponseSchema(BaseModel):
    user_id: UUID
    email: EmailStr
    profile_img: str | None = None
    role: str
    is_deleted: bool
    deleted_at: datetime | None = None
    created_by: UUID | None = None
    updated_by: UUID | None = None
    created_at: datetime
    updated_at: datetime

class UserLoginResponseSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    user: UserReadResponseSchema

class UserRegisterResponseSchema(UserLoginResponseSchema):
    pass