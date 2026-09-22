from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, String, Enum as SAEnum, DateTime, Boolean, Integer, JSON, CheckConstraint
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from datetime import datetime
from sqlalchemy import text
import uuid
from app.database import Base
from app.core.enums import ActivationStatus
from app.features.notifications.enums import NotificationStatus

class Notifications(Base):
    __tablename__ = "notifications"
    
    notification_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"), default=uuid.uuid4, nullable=False)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.user_id", ondelete="CASCADE"))
    title: Mapped[str]= mapped_column(String(100), nullable=False)
    description: Mapped[str | None]= mapped_column(String(500), nullable=True)
    file_storage_id: Mapped[uuid.UUID]= mapped_column(ForeignKey("file_storage.file_storage_id"), nullable=True)
    status: Mapped[ActivationStatus]= mapped_column(SAEnum(ActivationStatus, name='activation_status', native_enum= True), nullable=False, default=ActivationStatus.ENABLED, server_default="ENABLED")
    rollout_percentage: Mapped[int]= mapped_column(Integer, CheckConstraint("rollout_percentage>=0 AND rollout_percentage<=100"), nullable=False)
    redirect_link: Mapped[str | None]= mapped_column(String(500), nullable=True)
    is_deleted: Mapped[bool] = mapped_column( Boolean, default= False, server_default= text("false"))
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_by: Mapped[uuid.UUID]= mapped_column(ForeignKey("users.user_id"), nullable=True)
    updated_by: Mapped[uuid.UUID]= mapped_column(ForeignKey("users.user_id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now(), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now(), server_default=func.now(), onupdate=func.now(), nullable=False)
    

class NotificationHistory(Base):
    __tablename__ = "notification_history"

    notification_history_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"), default=uuid.uuid4, nullable=False)
    notification_id: Mapped[uuid.UUID]= mapped_column(ForeignKey("notifications.notification_id"), nullable=False)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.user_id", ondelete="CASCADE"))
    title: Mapped[str]= mapped_column(String(100), nullable=False)
    description: Mapped[str | None]= mapped_column(String(500), nullable=True)
    file_storage_id: Mapped[uuid.UUID]= mapped_column(ForeignKey("file_storage.file_storage_id"), nullable=True)
    status: Mapped[NotificationStatus]= mapped_column(SAEnum(NotificationStatus, name='notification_status', native_enum= True), nullable=False, default= NotificationStatus.PENDING, server_default="PENDING")  
    redirect_link: Mapped[str | None]= mapped_column(String(500), nullable=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now(), server_default=func.now(), nullable=False)
    delivery_channel: Mapped[str]= mapped_column(String(100), nullable=True)
    created_by: Mapped[uuid.UUID]= mapped_column(ForeignKey("users.user_id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now(), server_default=func.now(), nullable=False)