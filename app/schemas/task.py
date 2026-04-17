from pydantic import BaseModel, EmailStr, Field, ConfigDict

class TaskBase(BaseModel):
    task_name: str= Field(min_length=2, max_length=100)
    task_description: str | None = Field(default= None, max_length= 500 )
    task_status: str | None = Field(default= None, max_length= 50 )
    
class TaskCreate(TaskBase):
    user_id: int = Field()
    
class TaskUpdate(TaskBase):
    pass
    
class TaskRead(TaskCreate):
    task_id: int
    
    model_config=  ConfigDict(from_attributes= True)