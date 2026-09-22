from pydantic import BaseModel
from datetime import datetime
from uuid import UUID
from app.features.labels.enums import LabelOwner

class LabelCreateSchema(BaseModel):
    title: str
    description: str | None
    entity_type: str | None
    entity_id: UUID | None