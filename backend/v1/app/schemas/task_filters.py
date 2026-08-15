from pydantic import BaseModel
from typing import Optional
from ..models.enums import TaskPriority, TaskStatus

class TaskFilters(BaseModel):
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    search: Optional[str] = None