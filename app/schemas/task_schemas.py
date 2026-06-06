from pydantic import BaseModel, EmailStr, Field, ConfigDict
from ..models import TaskStatus

class TaskBase(BaseModel):
    task_name: str= Field(min_length=2, max_length=100)
    task_description: str | None = Field(default= None, max_length= 500 )
    task_status: TaskStatus | None = None
    
class TaskCreate(TaskBase):
    user_id: int | None = None
    
class TaskUpdate(BaseModel):
    task_name: str | None = Field(default = None, min_length=2, max_length=100)
    task_description: str | None = Field(default= None, max_length= 500 )
    task_status: TaskStatus | None = None
    
class TaskRead(TaskCreate):
    task_id: int
    
    model_config=  ConfigDict(from_attributes= True)