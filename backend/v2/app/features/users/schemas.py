from pydantic import BaseModel
from typing import EmailStr
from uuid import UUID

class UserCreateRequestSchema(BaseModel):
    email: EmailStr
    password: str
    image_url: str | None = None

class UserLoginRequestSchema(BaseModel):
    email: EmailStr
    password: str

class UserReadRequestSchema(BaseModel):
    user_id: UUID
    email: EmailStr
    image_url: str | None = None