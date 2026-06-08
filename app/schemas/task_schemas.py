from pydantic import BaseModel, Field, ConfigDict
from ..models import TaskStatus
from datetime import datetime
from uuid import UUID

class TaskBase(BaseModel):
    task_name: str= Field(min_length=2, max_length=100)
    task_description: str | None = Field(default= None, max_length= 500 )
    task_status: TaskStatus | None = None
    
class TaskCreate(TaskBase):
    user_id: UUID | None
    
class TaskUpdate(BaseModel):
    task_name: str | None = Field(default = None, min_length=2, max_length=100)
    task_description: str | None = Field(default= None, max_length= 500 )
    task_status: TaskStatus | None
    
class TaskRead(TaskCreate):
    task_id: UUID
    created_at: datetime
    updated_at: datetime
    created_by: UUID
    updated_by: UUID
    
    model_config=  ConfigDict(from_attributes= True)