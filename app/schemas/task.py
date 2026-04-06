from pydantic import BaseModel, EmailStr, Field, ConfigDict

class TaskCreate(BaseModel):
    task_name: str= Field(min_length=5, max_length=100)
    task_description: str | None = Field(default= None, max_length= 500 )
    
class TaskUpdate(TaskCreate):
    task_status: str| None = Field(default=None)
    
class TaskRead(BaseModel):
    task_id: int
    owner_id: int
    task_name: str
    task_description: str| None
    task_status: str
    
    model_config=  ConfigDict(from_attributes= True)