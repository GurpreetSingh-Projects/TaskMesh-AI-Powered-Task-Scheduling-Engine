from pydantic import BaseModel, Field, ConfigDict
from ..models import TaskStatus
from datetime import datetime
from uuid import UUID
from typing import Optional

class TaskBase(BaseModel):
    task_name: str= Field(min_length=2, max_length=100)
    task_description: str | None = Field(default= None, max_length= 500 )
    task_status: TaskStatus | None = None
    
class TaskCreate(TaskBase):
    user_id: UUID | None = None

class TaskUpdate(BaseModel):
    task_name: Optional[str]  = Field(default = None, min_length=2, max_length=100)
    task_description: Optional[str]  = Field(default= None, max_length= 500 )
    task_status: Optional[TaskStatus] 
    
class TaskRead(TaskCreate):
    task_id: UUID
    created_at: datetime
    updated_at: datetime
    created_by: UUID
    updated_by: UUID
    
    model_config=  ConfigDict(from_attributes= True)
    
class GetAllTasksResponse(BaseModel):
    items: list[TaskRead]
    total: int
    page: int
    page_size: int
    total_pages: int