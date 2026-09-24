from pydantic import BaseModel
from pydantic import EmailStr
from uuid import UUID
from datetime import datetime
from fastapi import UploadFile, Form

class UserLoginRequestSchema(BaseModel):
    email: EmailStr
    password: str

class UserReadResponseSchema(BaseModel):
    user_id: UUID
    full_name: str | None = None
    email: EmailStr
    profile_img: str | UUID | None = None
    role: str
    is_onboarding_completed: bool
    created_by: UUID | None = None
    updated_by: UUID | None = None
    created_at: datetime
    updated_at: datetime

class UserLoginResponseSchema(BaseModel):
    access_token: str
    access_token_expires_at: datetime
    refresh_token: str
    refresh_token_expires_at: datetime
    token_type: str
    user: UserReadResponseSchema
    user_settings: str

class UserRegisterResponseSchema(UserLoginResponseSchema):
    pass

class UserEditRequestSchema(BaseModel):
    email: EmailStr | None = None
    password: str | None = None
    full_name: str | None = None