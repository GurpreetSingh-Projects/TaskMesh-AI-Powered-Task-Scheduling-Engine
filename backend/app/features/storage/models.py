from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, String, Enum as SAEnum, DateTime, Boolean, Integer, JSON, BigInteger
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from datetime import datetime
from sqlalchemy import text
import uuid
from app.database import Base
from app.features.storage.enums import FileStorageEntity, ChecksumType


class FileStorage(Base):
    __tablename__ = "file_storage"

    file_storage_id:Mapped[PG_UUID]= mapped_column(PG_UUID(as_uuid= True), primary_key= True, server_default=text("gen_random_uuid()"))
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.user_id"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    size: Mapped[int] = mapped_column(BigInteger, nullable=False)
    type: Mapped[str] = mapped_column(String(100), nullable=False)
    entity_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    entity_type: Mapped[FileStorageEntity]= mapped_column(SAEnum(FileStorageEntity, name="file_storage_entity", native_enum= True), nullable= False)
    storage_key: Mapped[str] = mapped_column(String(1000), nullable=False)
    bucket_name: Mapped[str] = mapped_column(String(100), nullable=False)
    checksum_type: Mapped[ChecksumType] = mapped_column(SAEnum(ChecksumType, name="checksum_type", native_enum= True), default= ChecksumType.SHA256.value, nullable= False)
    checksum: Mapped[str] = mapped_column(String(32), nullable=False)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, server_default=text("false"))
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_by: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.user_id"), nullable=False)
    updated_by: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("users.user_id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now(), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now(), server_default=func.now(), onupdate=func.now(), nullable=False)