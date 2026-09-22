from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy import text, ForeignKey, String, Enum as SAEnum, DateTime, Boolean
from typing import List
from datetime import datetime
import uuid
from app.database import Base
from app.features.labels.enums import LabelOwner

class Labels(Base):
    __tablename__ = "labels"

    label_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"), default=uuid.uuid4, nullable=False)
    ownership: Mapped[LabelOwner]= mapped_column(SAEnum(LabelOwner, name="label_owner", native_enum=True), nullable=False, default=LabelOwner.SYSTEM, server_default="SYSTEM")
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.user_id"), nullable=False)
    title: Mapped[str]= mapped_column(String(100), nullable=False)
    description: Mapped[str | None]= mapped_column(String(500), nullable=True)
    file_storage_id: Mapped[uuid.UUID]= mapped_column(ForeignKey("file_storage.file_storage_id"), nullable=True)
    is_deleted: Mapped[bool] = mapped_column( Boolean, default= False, server_default= text("false"))
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    updated_by: Mapped[uuid.UUID]= mapped_column(ForeignKey("users.user_id"), nullable=True)
    created_by: Mapped[uuid.UUID]= mapped_column(ForeignKey("users.user_id"), nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now(), server_default=func.now(), onupdate=func.now(), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now(), server_default=func.now(), nullable=False)

class LabelMapping(Base):
    __tablename__ = "label_mapping"

    label_mapping_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"), default=uuid.uuid4, nullable=False)
    entity_type: Mapped[str]= mapped_column(String(100), nullable=False)
    entity_id: Mapped[uuid.UUID]= mapped_column(PG_UUID(as_uuid=True), nullable=False)
    label_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("labels.label_id"), nullable=False)
    updated_by: Mapped[uuid.UUID]= mapped_column(ForeignKey("users.user_id"), nullable=True)
    created_by: Mapped[uuid.UUID]= mapped_column(ForeignKey("users.user_id"), nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now(), server_default=func.now(), onupdate=func.now(), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now(), server_default=func.now(), nullable=False)