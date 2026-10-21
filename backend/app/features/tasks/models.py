from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, String, Enum as SAEnum, DateTime, Boolean, Integer, JSON, text, CheckConstraint
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from datetime import datetime
import uuid
from app.database import Base
from app.features.tasks.enums import TaskStatus, TaskPriority
from app.core.enums import ActivationStatus, DeliveryStatus

class Tasks(Base):
    __tablename__= "tasks"
    
    task_id: Mapped[uuid.UUID]= mapped_column(PG_UUID(as_uuid= True), primary_key=True, default=uuid.uuid4, server_default=text("gen_random_uuid()"), nullable=False)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.user_id", ondelete="CASCADE"))
    title: Mapped[str]= mapped_column(String(100), nullable=False)
    description: Mapped[str | None]= mapped_column(String(500), nullable=True)
    file_storage_id: Mapped[uuid.UUID]= mapped_column(ForeignKey("file_storage.file_storage_id"), nullable=True)
    status: Mapped[TaskStatus] = mapped_column(SAEnum(TaskStatus, name="task_status", native_enum= True), nullable=False, default=TaskStatus.PENDING, server_default="PENDING")
    completed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    due_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    priority: Mapped[TaskPriority] = mapped_column(SAEnum(TaskPriority, name= "task_priority", native_enum= True), nullable= False, default= TaskPriority.NORMAL, server_default = "NORMAL" )
    is_deleted: Mapped[bool] = mapped_column( Boolean, default= False, server_default= text('false'))
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    updated_by: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.user_id"), default=None, nullable=True)
    created_by: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.user_id"), default=None, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now(), server_default=func.now(), nullable=True, onupdate=func.now())
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now(), server_default=func.now(), nullable=True)
    
class SubTasks(Base):
    __tablename__= "subtasks"
    
    subtask_id: Mapped[uuid.UUID]= mapped_column(PG_UUID(as_uuid= True), primary_key=True, default=uuid.uuid4, server_default=text("gen_random_uuid()"), nullable=False)
    task_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("tasks.task_id", ondelete="CASCADE"))
    title: Mapped[str]= mapped_column(String(100), nullable=False)
    description: Mapped[str | None]= mapped_column(String(500), nullable=True)
    file_storage_id: Mapped[uuid.UUID]= mapped_column(ForeignKey("file_storage.file_storage_id"), nullable=True)
    status: Mapped[TaskStatus] = mapped_column(SAEnum(TaskStatus, name="task_status", native_enum= True), nullable=False, default=TaskStatus.PENDING, server_default="PENDING")
    completed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    due_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    priority: Mapped[TaskPriority] = mapped_column(SAEnum(TaskPriority, name= "task_priority", native_enum= True), nullable= False, default= TaskPriority.NORMAL, server_default = "NORMAL" )
    is_deleted: Mapped[bool] = mapped_column( Boolean, default= False, server_default= text('false'))
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    updated_by: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.user_id"), default=None, nullable=True)
    created_by: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.user_id"), default=None, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now(), server_default=func.now(), nullable=True, onupdate=func.now())
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now(), server_default=func.now(), nullable=True)
    
class TaskReminderConfig(Base):
    __tablename__= "task_reminder_config"
    
    task_reminder_config_id: Mapped[uuid.UUID]= mapped_column(PG_UUID(as_uuid= True), primary_key=True, default=uuid.uuid4, server_default=text("gen_random_uuid()"), nullable=False)
    task_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("tasks.task_id", ondelete="CASCADE"), nullable=True)
    subtask_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("subtasks.subtask_id", ondelete="CASCADE"), nullable=True)
    status: Mapped[ActivationStatus]= mapped_column(SAEnum(ActivationStatus, name='activation_status', native_enum= True), nullable=False, default=ActivationStatus.ENABLED, server_default="ENABLED")
    delivery_channel: Mapped[list]= mapped_column(JSON, nullable=True)
    interval_minutes: Mapped[int]= mapped_column(Integer, CheckConstraint("interval_minutes>=0 AND interval_minutes<=525960"), nullable=False)
    attempts: Mapped[int]= mapped_column(Integer, default=0, nullable=False)
    max_attempts: Mapped[int]= mapped_column(Integer, default=0, nullable=False)
    is_deleted: Mapped[bool] = mapped_column( Boolean, default= False, server_default= text('false'))
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    updated_by: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.user_id"), default=None, nullable=True)
    created_by: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.user_id"), default=None, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now(), server_default=func.now(), nullable=True, onupdate=func.now())
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now(), server_default=func.now(), nullable=True)
    
class TaskReminderActivity(Base):
    __tablename__= "task_reminder_activity"
    
    task_reminder_activity_id: Mapped[uuid.UUID]= mapped_column(PG_UUID(as_uuid= True), primary_key=True, default=uuid.uuid4, server_default=text("gen_random_uuid()"), nullable=False)
    task_reminder_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("task_reminder_config.task_reminder_config_id", ondelete="CASCADE"), nullable=True)
    task_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("tasks.task_id", ondelete="CASCADE"), nullable=True)    
    subtask_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("subtasks.subtask_id", ondelete="CASCADE"), nullable=True)    
    delivery_status: Mapped[DeliveryStatus]= mapped_column(SAEnum(DeliveryStatus, name='delivery_status', native_enum= True), nullable=False, default=DeliveryStatus.PENDING, server_default="PENDING")
    delivery_channel: Mapped[str]= mapped_column(String(100), nullable=True)
    attempt_count: Mapped[int]= mapped_column(Integer, default=0, nullable=False)
    retry_remaining: Mapped[int]= mapped_column(Integer, default=3, nullable=False)
    title: Mapped[str]= mapped_column(String(100), nullable=False)
    description: Mapped[str | None]= mapped_column(String(500), nullable=True)
    file_storage_id: Mapped[uuid.UUID]= mapped_column(ForeignKey("file_storage.file_storage_id"), nullable=True)
    reated_by: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.user_id"), default=None, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now(), server_default=func.now(), nullable=True)
