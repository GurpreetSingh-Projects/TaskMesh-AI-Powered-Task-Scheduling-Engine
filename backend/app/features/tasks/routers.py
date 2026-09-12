from fastapi import APIRouter, Depends, Query
from uuid import UUID
from app.core.dependencies import get_current_user
from app.features.tasks.dependencies import get_tasks_service
from app.features.tasks.schemas import TaskCreateRequestSchema, TaskUpdateRequestSchema, TaskReadResponseItemSchema, TaskReadResponseSchema
from app.features.tasks.services import TaskService

router = APIRouter(prefix="/tasks", tags=["Tasks"], dependencies=[Depends(get_current_user)])

@router.post("", response_model=TaskReadResponseItemSchema, status_code=201, summary="Create a new task")
async def create_task(task_data: TaskCreateRequestSchema, user= Depends(get_current_user), task_service: TaskService = Depends(get_tasks_service)):
    response = await task_service.create_task(user=user, task_data=task_data)
    return response

@router.get("", response_model= TaskReadResponseSchema, summary="List your tasks")
async def get_tasks(limit: int = Query(15, ge=0, le= 500), offset:int= Query(0, ge= 0), user= Depends(get_current_user), task_service: TaskService = Depends(get_tasks_service)):
    response= await task_service.get_tasks(user= user, limit= limit, offset= offset)
    return response

@router.patch("/{task_id}", response_model=TaskReadResponseItemSchema, summary="Update a task")
async def update_task(task_id: UUID, task_data: TaskUpdateRequestSchema, user= Depends(get_current_user), task_service: TaskService = Depends(get_tasks_service)):
    response= await task_service.update_task(user= user, task_id= task_id, task_data= task_data)
    return response

@router.patch("/deactivate/{task_id}", status_code= 204, summary= "Delete a task")
async def delete_task(task_id: UUID, user= Depends(get_current_user), task_service: TaskService = Depends(get_tasks_service)):
    response =  await task_service.delete_task(user_id= user.user_id, task_id= task_id)
    return response