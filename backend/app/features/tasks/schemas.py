from pydantic import BaseModel
from datetime import datetime
from uuid import UUID
from app.features.tasks.enums import TaskStatus, TaskPriority

# Tasks

class TaskBaseResponse(BaseModel):
    title: str
    description: str | None
    file_storage_id: UUID | None
    image_url: str | None
    status: TaskStatus
    completed_at: datetime | None
    due_at: datetime | None
    priority: TaskPriority
    updated_by: UUID | None
    created_by: UUID | None
    updated_at: datetime
    created_at: datetime

class TaskReadResponseItemSchema(TaskBaseResponse):
    task_id: UUID
    user_id: UUID

class TaskReadResponseSchema(BaseModel):
    items: list[TaskReadResponseItemSchema]
    limit: int
    offset: int
    has_more: bool
    total_tasks: int
    page: int
    total_pages: int
    
class TaskCreateRequestSchema(BaseModel):
    title: str
    description: str | None
    status: TaskStatus
    priority: TaskPriority
    completed_at: datetime | None
    due_at: datetime | None

class TaskUpdateRequestSchema(TaskCreateRequestSchema):
    title: str | None
    description: str | None
    status: TaskStatus | None
    priority: TaskPriority | None
    completed_at: datetime | None
    due_at: datetime | None

# Subtasks
class SubtaskReadResponseItemSchema(TaskBaseResponse):
    task_id: UUID
    subtask_id: UUID

class SubtaskReadResponseSchema(BaseModel):
    items: list[SubtaskReadResponseItemSchema]
    limit: int
    offset: int
    has_more: bool
    total_subtasks: int
    page: int
    total_pages: int
    
class SubtaskCreateRequestSchema(TaskCreateRequestSchema):
    task_id: UUID

class SubtaskUpdateRequestSchema(TaskUpdateRequestSchema):
    pass