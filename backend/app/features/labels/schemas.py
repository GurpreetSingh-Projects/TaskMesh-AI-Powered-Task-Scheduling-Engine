from pydantic import BaseModel, ConfigDict
from datetime import datetime
from uuid import UUID
from app.features.labels.enums import LabelOwner

class LabelCreateSchema(BaseModel):
    title: str
    description: str | None
    entity_type: str | None
    entity_id: UUID | None

class LabelResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    label_id: UUID
    title: str
    user_id: UUID
    description: str | None
    updated_by: UUID | None
    ownership: str
    image_url: str | None

class GetLabelsSchema(BaseModel):
    items: list[LabelResponseSchema]