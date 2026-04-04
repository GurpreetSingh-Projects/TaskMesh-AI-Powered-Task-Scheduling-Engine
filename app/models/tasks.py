from sqlalchemy.orm import Mapped,mapped_column, relationship
from sqlalchemy import ForeignKey, String, Integer, text
from .base import Base

class Task(Base):
    __tablename__= "tasks"
    
    task_id: Mapped[int]= mapped_column(Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id", ondelete="CASCADE"))
    task_name: Mapped[str]= mapped_column(String(100), nullable=False)
    task_description: Mapped[str| None]= mapped_column(String(500), nullable=True)
    task_status: Mapped[str] = mapped_column(String(50), nullable=False, default="pending", server_default="pending")
    
    owner:Mapped["User"] = relationship("User", back_populates="tasks")