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
    title: str = Form(...),
    description: str | None = Form(None),
    status: TaskStatus = Form(None),
    priority: TaskPriority = Form(None),
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

@router.get("/summary", summary="List your tasks")
async def get_tasks(
    limit: int = Query(10, ge=1, le=500),
    user=Depends(get_current_user),
    task_service: TaskService = Depends(get_tasks_service),
):
    return await task_service.get_tasks_summary(
        user=user, limit=limit,
    )

@router.get("", response_model=TaskReadResponseSchema, summary="List your tasks")
async def get_tasks(
    start_date: datetime= Query(default= datetime.now()),
    end_date: datetime | None = Query(default= datetime.now()),
    status: TaskStatus | None = None,
    limit: int = Query(15, ge=1, le=500),
    offset: int = Query(0, ge=0),
    user=Depends(get_current_user),
    task_service: TaskService = Depends(get_tasks_service),
):
    return await task_service.get_tasks(
        status=status, start_date=start_date, end_date=end_date,
        user=user, limit=limit, offset=offset,
    )

@router.patch("/{task_id}", response_model=TaskReadResponseItemSchema, summary="Update a task",
)
async def update_task(
    task_id: UUID,
    title: str | None = Form(None),
    description: str | None = Form(None),
    status: TaskStatus | None = Form(None),
    priority: TaskPriority | None = Form(None),
    due_at: datetime | None = Form(None),
    completed_at: datetime | None = Form(None),
    task_img: UploadFile | None = File(None),
    user=Depends(get_current_user),
    task_service: TaskService = Depends(get_tasks_service),
):
    task_data = TaskUpdateRequestSchema(
        title=title,
        description=description,
        status=status,
        priority=priority,
        due_at=due_at,
        completed_at=completed_at,
    )

    response = await task_service.update_task(
        user=user,
        task_id=task_id,
        task_data=task_data,
        task_img=task_img,
    )

    return response

@router.patch("/deactivate/{task_id}", status_code= 204, summary= "Deactivate task with its task_id")
async def deactivate_task(task_id: UUID, user= Depends(get_current_user), task_service: TaskService = Depends(get_tasks_service)):
    await task_service.deactivate_task(user= user, task_id= task_id)

# Subtasks
@router.post("/subtask/", response_model= SubtaskReadResponseItemSchema, status_code=201, summary="Create a new subtask")
async def create_subtask(
    task_id: UUID= Form(...),
    title: str = Form(...),
    description: str | None = Form(None),
    status: TaskStatus = Form(...),
    priority: TaskPriority = Form(...),
    due_at: datetime | None = Form(None),
    completed_at: datetime | None = Form(None),
    subtask_img: UploadFile | None = File(None),
    user= Depends(get_current_user), 
    task_service: TaskService = Depends(get_tasks_service)):
    subtask_data = SubtaskCreateRequestSchema(
            task_id= task_id,
            title=title,
            description=description,
            status=status,
            priority=priority,
            due_at=due_at,
            completed_at=completed_at,
        )
    response = await task_service.create_subtask(user= user, subtask_data= subtask_data, subtask_img= subtask_img)
    return response

@router.get("/subtasks/", response_model= SubtaskReadResponseSchema, summary="List subtasks for a given task id")
async def get_subtasks(task_id: UUID, limit: int = Query(15, ge=0, le= 500), offset:int= Query(0, ge= 0), user= Depends(get_current_user), task_service: TaskService = Depends(get_tasks_service)):
    response= await task_service.get_subtasks(user= user, task_id= task_id, limit= limit, offset= offset)
    return response


@router.patch(
    "/subtasks/{subtask_id}",
    response_model=SubtaskReadResponseItemSchema,
    summary="Update a subtask",
)
async def update_subtask(
    subtask_id: UUID,
    title: str | None = Form(None),
    description: str | None = Form(None),
    status: TaskStatus | None = Form(None),
    priority: TaskPriority | None = Form(None),
    due_at: datetime | None = Form(None),
    completed_at: datetime | None = Form(None),
    subtask_img: UploadFile | None = File(None),
    user=Depends(get_current_user),
    task_service: TaskService = Depends(get_tasks_service),
):
    subtask_data = SubtaskUpdateRequestSchema(
        title=title,
        description=description,
        status=status,
        priority=priority,
        due_at=due_at,
        completed_at=completed_at,
    )

    response = await task_service.update_subtask(
        user=user,
        subtask_id=subtask_id,
        subtask_data=subtask_data,
        subtask_img=subtask_img,
    )

    return response

@router.patch("/subtask/deactivate/{subtask_id}/", status_code= 204, summary= "Deactivate task with its task_id")
async def deactivate_subtask(subtask_id: UUID, user= Depends(get_current_user), task_service: TaskService = Depends(get_tasks_service)):
    await task_service.deactivate_subtask(user= user, subtask_id= subtask_id)