from fastapi import APIRouter, Depends, Query, UploadFile, Form, File
from uuid import UUID
from typing import Annotated
from app.core.dependencies import get_current_user
from app.features.tasks.dependencies import get_tasks_service
from app.features.tasks.schemas import TaskCreateRequestSchema, TaskUpdateRequestSchema, TaskReadResponseItemSchema, TaskReadResponseSchema, SubtaskReadResponseItemSchema, SubtaskReadResponseSchema, SubtaskCreateRequestSchema, SubtaskUpdateRequestSchema
from app.features.tasks.services import TaskService
from app.features.tasks.enums import TaskPriority, TaskStatus
from datetime import datetime

router = APIRouter(prefix="/tasks", tags=["Tasks & Subtasks"], dependencies=[Depends(get_current_user)])

# Tasks
@router.post("", response_model=TaskReadResponseItemSchema, status_code=201, summary="Create a new task")
async def create_task(
    # task_data: TaskCreateRequestSchema,
    title: str = Form(...),
    description: str | None = Form(None),
    status: TaskStatus = Form(...),
    priority: TaskPriority = Form(...),
    due_at: datetime | None = Form(None),
    completed_at: datetime | None = Form(None),
    task_img: UploadFile | None = File(None),
    user= Depends(get_current_user), 
    task_service: TaskService = Depends(get_tasks_service)
):
    task_data = TaskCreateRequestSchema(
        title=title,
        description=description,
        status=status,
        priority=priority,
        due_at=due_at,
        completed_at=completed_at,
    )
    response = await task_service.create_task(user=user, task_img=task_img, task_data=task_data)
    return response

@router.get("", response_model= TaskReadResponseSchema, summary="List your tasks")
async def get_tasks(limit: int = Query(15, ge=0, le= 500), offset:int= Query(0, ge= 0), user= Depends(get_current_user), task_service: TaskService = Depends(get_tasks_service)):
    response= await task_service.get_tasks(user= user, limit= limit, offset= offset)
    return response

@router.patch("/{task_id}", response_model=TaskReadResponseItemSchema, summary="Update a task")
async def update_task(task_id: UUID, task_data: TaskUpdateRequestSchema, user= Depends(get_current_user), task_service: TaskService = Depends(get_tasks_service)):
    response= await task_service.update_task(user= user, task_id= task_id, task_data= task_data)
    return response

@router.patch("/deactivate/{task_id}", status_code= 204, summary= "Deactivate task with its task_id")
async def deactivate_task(task_id: UUID, user= Depends(get_current_user), task_service: TaskService = Depends(get_tasks_service)):
    await task_service.deactivate_task(user= user, task_id= task_id)

# Subtasks
@router.post("/subtask/", response_model= SubtaskReadResponseItemSchema, status_code=201, summary="Create a new subtask")
async def create_subtask(subtask_data: SubtaskCreateRequestSchema, user= Depends(get_current_user), task_service: TaskService = Depends(get_tasks_service)):
    response = await task_service.create_subtask(user= user, subtask_data= subtask_data)
    return response

@router.get("/subtasks", response_model= SubtaskReadResponseSchema, summary="List subtasks for a given task id")
async def get_subtasks(task_id: UUID, limit: int = Query(15, ge=0, le= 500), offset:int= Query(0, ge= 0), user= Depends(get_current_user), task_service: TaskService = Depends(get_tasks_service)):
    response= await task_service.get_subtasks(user= user, task_id= task_id, limit= limit, offset= offset)
    return response

@router.patch("/subtask/{subtask_id}", response_model= SubtaskReadResponseItemSchema, summary="Update subtask by its id")
async def update_task(subtask_id: UUID, subtask_data: SubtaskUpdateRequestSchema, user= Depends(get_current_user), task_service: TaskService = Depends(get_tasks_service)):
    response= await task_service.update_subtask(user= user, subtask_id= subtask_id, subtask_data= subtask_data)
    return response

@router.patch("/subtask/deactivate/{subtask_id}/", status_code= 204, summary= "Deactivate task with its task_id")
async def deactivate_subtask(subtask_id: UUID, user= Depends(get_current_user), task_service: TaskService = Depends(get_tasks_service)):
    await task_service.deactivate_subtask(user= user, subtask_id= subtask_id)