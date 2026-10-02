from pydantic import BaseModel
from pydantic import EmailStr, ConfigDict
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
    is_profile_completed: bool
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

class UserSettingsReadSchema(BaseModel):
    user_settings_id: UUID
    user_id: UUID | None
    needs_reminders: bool
    timezone: str | None
    notification_enabled: bool | None
    preferred_lang: list[str]
    available_lang: list[str]
    theme: str
    supported_image_formats: list[str]
    max_image_dimension: int | None
    image_conversion_format: str | None
    image_quality: float | None

    model_config = ConfigDict(from_attributes=True)