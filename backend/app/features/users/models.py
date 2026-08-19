from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, String, Enum as SAEnum, DateTime, Boolean, Integer, JSON
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from datetime import datetime
from sqlalchemy import text
import uuid
from app.database import Base
from app.features.users.enums import UserRoles

class Users(Base):
    __tablename__ = "users"
    
    user_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"), default=uuid.uuid4, nullable=False)
    full_name: Mapped[str] = mapped_column(String(100), nullable=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    profile_img: Mapped[str] = mapped_column(String, unique=True, nullable=True)
    hashed_pswd: Mapped[str]= mapped_column(String(255), nullable=False)
    role: Mapped[UserRoles] = mapped_column(SAEnum( UserRoles, name= "user_role", native_enum = True ), default=UserRoles.USER, server_default="USER")
    is_onboarding_completed: Mapped[bool] = mapped_column(Boolean, default= False, server_default=text("false"))
    is_deleted: Mapped[bool] = mapped_column( Boolean, default= False, server_default= text("false"))
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_by: Mapped[uuid.UUID]= mapped_column(ForeignKey("users.user_id"), nullable=True)
    updated_by: Mapped[uuid.UUID]= mapped_column(ForeignKey("users.user_id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now(), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now(), server_default=func.now(), onupdate=func.now(), nullable=False)
    version_number: Mapped[int] = mapped_column(Integer, default=0)
    
class UserSettings(Base):
  __tablename__ = "user_settings"
  
  user_settings_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"), default=uuid.uuid4, nullable=False)
  user_id: Mapped[uuid.UUID]= mapped_column(ForeignKey("users.user_id"), nullable=False)
  needs_reminders: Mapped[bool] = mapped_column( Boolean, default= False, server_default= text("false"))
  timezone: Mapped[str]= mapped_column(String(255), default='Asia/Kolkata', nullable=False)
  notification_enabled: Mapped[bool]= mapped_column(Boolean, default=True, nullable=False)
  preferred_lang: Mapped[list]= mapped_column(JSON, default=["en"])
  available_lang: Mapped[list]= mapped_column(JSON, default=["en"])
  theme: Mapped[str]= mapped_column(String(25), default='light')
  is_deleted: Mapped[bool] = mapped_column( Boolean, default= False, server_default= text("false"))
  deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
  created_by: Mapped[uuid.UUID]= mapped_column(ForeignKey("users.user_id"), nullable=True)
  updated_by: Mapped[uuid.UUID]= mapped_column(ForeignKey("users.user_id"), nullable=True)
  created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now(), server_default=func.now(), nullable=False)
  updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now(), server_default=func.now(), onupdate=func.now(), nullable=False)