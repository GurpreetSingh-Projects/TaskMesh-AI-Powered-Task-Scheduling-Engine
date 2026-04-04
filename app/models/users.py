from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer
from typing import List
from .base import Base

class User(Base):
    __tablename__ = "users"
    
    user_id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True, nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    hashed_pswd: Mapped[str]= mapped_column(String(255), nullable=False)
    tasks: Mapped[List["Task"]] = relationship(back_populates="owner", cascade="all, delete-orphan")