from sqlalchemy.orm import Mapped,mapped_column, relationship
from sqlalchemy import ForeignKey, String, Integer, text, Enum as SAEnum, DateTime
from sqlalchemy.sql import func
from datetime import datetime
from app.models.users import User
from .base import Base
from .enums import TaskStatus
    
class Task(Base):
    __tablename__= "tasks"
    
    task_id: Mapped[int]= mapped_column(Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id", ondelete="CASCADE"))
    task_name: Mapped[str]= mapped_column(String(100), nullable=False)
    task_description: Mapped[str| None]= mapped_column(String(500), nullable=True)
    task_status: Mapped[TaskStatus] = mapped_column(SAEnum(TaskStatus, name="task_status_enum", native_enum= True), nullable=False, default=TaskStatus.pending.value, server_default=TaskStatus.pending.value)
    
    updated_by: Mapped[int] = mapped_column(ForeignKey("users.user_id"), default=None, nullable=True)
    created_by: Mapped[int] = mapped_column(ForeignKey("users.user_id"), default=None, nullable=True)
    
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now(), server_default=func.now(), nullable=True, onupdate=func.now())
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now(), server_default=func.now(), nullable=True)
    
    owner: Mapped["User"] = relationship("User", back_populates="tasks", foreign_keys=[user_id])
    creator: Mapped["User"] = relationship("User", foreign_keys=[created_by])
    updater: Mapped["User"] = relationship("User", foreign_keys=[updated_by])