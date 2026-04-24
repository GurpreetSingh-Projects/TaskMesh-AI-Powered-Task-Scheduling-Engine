from sqlalchemy.orm import Mapped,mapped_column, relationship
from sqlalchemy import ForeignKey, String, Integer, text, Enum as SAEnum
from .base import Base
from .enums import TaskStatus

class Task(Base):
    __tablename__= "tasks"
    
    task_id: Mapped[int]= mapped_column(Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id", ondelete="CASCADE"))
    task_name: Mapped[str]= mapped_column(String(100), nullable=False)
    task_description: Mapped[str| None]= mapped_column(String(500), nullable=True)
    task_status: Mapped[TaskStatus] = mapped_column(SAEnum(TaskStatus, name="task_status_enum", native_enum= True), nullable=False, default=TaskStatus.pending.value, server_default=TaskStatus.pending.value)
    
    owner:Mapped["User"] = relationship("User", back_populates="tasks")