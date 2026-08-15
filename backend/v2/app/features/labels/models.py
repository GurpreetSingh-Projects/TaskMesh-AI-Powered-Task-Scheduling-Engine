from sqlalchemy import ForeignKey, String, Enum as SAEnum, DateTime, Boolean
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from typing import List
from datetime import datetime
from ...database import Base
from sqlalchemy import text
import uuid

Table users {
  role varchar
  needs_reminders boolean
  version_number int
}

class User(Base):
    __tablename__ = "users"
    
    user_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"), default=uuid.uuid4, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    hashed_pswd: Mapped[str]= mapped_column(String(255), nullable=False)
    role: Mapped[UserRoles] = mapped_column(SAEnum( UserRoles, name= "user_role", native_enum = True ), default=UserRoles.USER, server_default="USER")
    needs_reminders: Mapped[bool] = mapped_column( Boolean, default= False, server_default= text("false"))
    is_deleted: Mapped[bool] = mapped_column( Boolean, default= False, server_default= text("false"))
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    updated_by: Mapped[uuid.UUID]= mapped_column(ForeignKey("users.user_id"), nullable=True)
    created_by: Mapped[uuid.UUID]= mapped_column(ForeignKey("users.user_id"), nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now(), server_default=func.now(), onupdate=func.now(), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now(), server_default=func.now(), nullable=False)
    version_number