from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Enum as SAEnum
from typing import List
from .base import Base
from .user_roles import UserRoles

class User(Base):
    __tablename__ = "users"
    
    user_id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True, nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    hashed_pswd: Mapped[str]= mapped_column(String(255), nullable=False)
    role: Mapped[UserRoles] = mapped_column(SAEnum( UserRoles, name= "user_role", native_enum = True ), default=UserRoles.USER, server_default="USER")
    tasks: Mapped[List["Task"]] = relationship(back_populates="owner", cascade="all, delete-orphan")