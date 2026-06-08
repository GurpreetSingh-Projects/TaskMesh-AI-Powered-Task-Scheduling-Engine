from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, Integer, Enum as SAEnum, DateTime
from sqlalchemy.sql import func
from typing import List
from datetime import datetime
from .base import Base
from .user_roles import UserRoles

class User(Base):
    __tablename__ = "users"
    
    user_id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True, nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    hashed_pswd: Mapped[str]= mapped_column(String(255), nullable=False)
    role: Mapped[UserRoles] = mapped_column(SAEnum( UserRoles, name= "user_role", native_enum = True ), default=UserRoles.USER, server_default="USER")
    
    updated_by: Mapped[int]= mapped_column(ForeignKey("users.user_id"), nullable=True)
    created_by: Mapped[int]= mapped_column(ForeignKey("users.user_id"), nullable=True)
    
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now(), server_default=func.now(), onupdate=func.now(), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now(), server_default=func.now(), nullable=False)
    
    tasks: Mapped[List["Task"]] = relationship("Task", back_populates="owner", foreign_keys="Task.user_id", cascade="all, delete-orphan")