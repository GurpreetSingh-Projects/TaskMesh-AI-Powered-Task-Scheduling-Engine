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

    model_config = ConfigDict(from_attributes=True)

class UserLoginResponseSchema(BaseModel):
    access_token: str
    access_token_expires_at: datetime
    refresh_token: str
    refresh_token_expires_at: datetime
    token_type: str
    user: UserReadResponseSchema
    user_settings: str

    model_config = ConfigDict(from_attributes=True)

class UserRegisterResponseSchema(UserLoginResponseSchema):
    pass

class UserEditRequestSchema(BaseModel):
    email: EmailStr | None = None
    password: str | None = None
    full_name: str | None = None

class UserSettingsCreateRequestSchema(BaseModel):
    needs_reminders: bool | None = None
    timezone: str | None = None
    notification_enabled: bool | None = None
    preferred_lang: list[str] | None = None
    theme: str | None = None

class UserSettingsReadResponseSchema(BaseModel):
    user_settings_id: UUID
    user_id: UUID
    needs_reminders: bool | None
    timezone: str | None
    notification_enabled: bool | None
    preferred_lang: list[str] | None
    available_lang: list[str] | None
    theme: str | None
    supported_media_types: list[str] | None
    max_media_size: int | None
    max_image_width: int | None
    image_conversion_format: str | None
    image_quality: float | None
    created_by: UUID | None
    updated_by: UUID | None
    created_at: datetime | None
    updated_at: datetime | None

    model_config = ConfigDict(from_attributes=True)