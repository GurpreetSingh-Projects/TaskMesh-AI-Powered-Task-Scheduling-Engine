from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, String, Enum as SAEnum, DateTime, Boolean, Integer, JSON
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from datetime import datetime
from sqlalchemy import text
import uuid
from app.database import Base
from app.features.users.enums import UserActivityType

class UserActivity(Base):
  __tablename__ = "user_activity"
    
  user_activity_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"), default=uuid.uuid4, nullable=False)
  user_id: Mapped[uuid.UUID]= mapped_column(ForeignKey("users.user_id"), nullable=False)
  timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now(), server_default=func.now(), nullable=False)
  activity_type: Mapped[UserActivityType]= mapped_column(SAEnum)
  task_id: Mapped[uuid.UUID]= mapped_column(ForeignKey("tasks.task_id"), nullable=False)
  subtask_id: Mapped[uuid.UUID]= mapped_column(ForeignKey("subtasks.subtask_id"), nullable=False)
  device_id: Mapped[str]= mapped_column(String(100), nullable=False)
  ip_address: Mapped[str]= mapped_column(String(100), default='0.0.0.0', nullable=False)
  is_deleted: Mapped[bool] = mapped_column( Boolean, default= False, server_default= text("false"))
  deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
  created_by: Mapped[uuid.UUID]= mapped_column(ForeignKey("users.user_id"), nullable=True)
  updated_by: Mapped[uuid.UUID]= mapped_column(ForeignKey("users.user_id"), nullable=True)
  created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now(), server_default=func.now(), nullable=False)
  updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now(), server_default=func.now(), onupdate=func.now(), nullable=False)