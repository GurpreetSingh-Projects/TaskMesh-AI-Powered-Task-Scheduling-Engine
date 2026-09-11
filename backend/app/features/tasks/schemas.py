from pydantic import BaseModel
from datetime import datetime
from uuid import UUID
from app.features.tasks.enums import TaskStatus, TaskPriority

class TaskReadResponseSchema(BaseModel):
    task_id: UUID
    user_id: UUID
    title: str
    description: str | None
    image_url: str | None
    status: str
    completed_at: datetime | None
    due_at: datetime | None
    priority: TaskPriority
    updated_by: UUID | None
    created_by: UUID | None
    updated_at: datetime
    created_at: datetime

class TaskCreateRequestSchema(BaseModel):
    title: str
    description: str | None
    image_url: str | None
    status: TaskStatus
    priority: TaskPriority
    completed_at: datetime | None
    due_at: datetime | None

class TaskUpdateRequestSchema(TaskCreateRequestSchema):
    pass