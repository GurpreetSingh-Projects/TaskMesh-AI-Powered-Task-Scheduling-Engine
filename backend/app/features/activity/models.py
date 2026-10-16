from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, String, Enum as SAEnum, DateTime, Boolean, Integer, JSON
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from datetime import datetime
from sqlalchemy import text
import uuid
from app.database import Base
from app.features.activity.enums import UserActivityType, ActivityEntityType

class UserActivity(Base):
  __tablename__ = "user_activity"

  user_activity_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"), default=uuid.uuid4)
  user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.user_id"))
  # user_device_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("user_devices.user_device_id"))
  user_device_id: Mapped[str | None] = mapped_column(String(50))
  timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
  activity_type: Mapped[UserActivityType] = mapped_column(SAEnum(UserActivityType, name="user_activity_type", native_enum=True))
  entity_type: Mapped[ActivityEntityType | None] = mapped_column(SAEnum(ActivityEntityType, name= "activity_entity_type",native_enum= True))
  entity_id: Mapped[uuid.UUID | None] = mapped_column(PG_UUID(as_uuid=True))
  is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, server_default=text("false"))
  deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
  created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
  created_by: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("users.user_id"))
  updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
  updated_by: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("users.user_id"))