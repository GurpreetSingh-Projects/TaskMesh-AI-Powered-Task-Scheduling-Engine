from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict
from app.features.activity.enums import UserActivityType


class UserActivityCreateRequestSchema(BaseModel):
    activity_type: UserActivityType
    user_device_id: str | None = None
    entity_type: str | None = None
    entity_id: UUID | None = None

class UserActivityReadResponseSchema(BaseModel):
    user_activity_id: UUID
    user_id: UUID
    user_device_id: str | None
    timestamp: datetime
    activity_type: UserActivityType
    entity_type: str | None
    entity_id: UUID | None
    is_deleted: bool
    deleted_at: datetime | None
    created_at: datetime
    created_by: UUID | None
    updated_at: datetime
    updated_by: UUID | None

    model_config = ConfigDict(from_attributes=True)