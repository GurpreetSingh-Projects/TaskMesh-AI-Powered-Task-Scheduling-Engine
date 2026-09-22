from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime
from datetime import datetime
from app.features.storage.enums import FileStorageEntity

class FileReadResponseItemSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    file_storage_id: UUID
    user_id: UUID
    name: str
    size: int
    type: str
    entity_id: UUID
    entity_type: FileStorageEntity
    storage_key: str
    md5_checksum: str
    download_url: str | None = None
    is_deleted: bool
    deleted_at: datetime | None
    created_by: UUID
    updated_by: UUID | None
    created_at: datetime
    updated_at: datetime

class FileReadResponseSchema(BaseModel):
    detail: str
    item: FileReadResponseItemSchema