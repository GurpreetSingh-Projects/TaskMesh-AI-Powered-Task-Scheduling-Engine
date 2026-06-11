from sqlalchemy.orm import Mapped,mapped_column, relationship
from sqlalchemy import ForeignKey, String, text, Enum as SAEnum, DateTime, Boolean
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from datetime import datetime
from app.models.users import User
from .base import Base
from .enums import TaskStatus, TaskPriority
from sqlalchemy import text
import uuid

class Task(Base):
    __tablename__= "tasks"
    
    task_id: Mapped[uuid.UUID]= mapped_column(PG_UUID(as_uuid= True), primary_key=True, default=uuid.uuid4, server_default=text("gen_random_uuid()"), nullable=False)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.user_id", ondelete="CASCADE"))
    task_name: Mapped[str]= mapped_column(String(100), nullable=False)
    task_description: Mapped[str | None]= mapped_column(String(500), nullable=True)
    task_status: Mapped[TaskStatus] = mapped_column(SAEnum(TaskStatus, name="task_status_enum", native_enum= True), nullable=False, default=TaskStatus.pending, server_default="pending")
    updated_by: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.user_id"), default=None, nullable=True)
    created_by: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.user_id"), default=None, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now(), server_default=func.now(), nullable=True, onupdate=func.now())
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now(), server_default=func.now(), nullable=True)
    is_deleted: Mapped[bool] = mapped_column( Boolean, default= False, server_default= text('false'))
    task_completed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    expected_completion_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    priority: Mapped[TaskPriority] = mapped_column(SAEnum(TaskPriority, name= "task_priority_enum", native_enum= True), nullable= False, default= TaskPriority.normal, server_default = "normal" )
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    owner: Mapped["User"] = relationship("User", back_populates="tasks", foreign_keys=[user_id])
    creator: Mapped["User"] = relationship("User", foreign_keys=[created_by])
    updater: Mapped["User"] = relationship("User", foreign_keys=[updated_by])