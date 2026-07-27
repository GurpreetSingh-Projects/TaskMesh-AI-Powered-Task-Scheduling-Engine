from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional, Annotated
from uuid import UUID
from ..models import UserRoles, TaskStatus
from ..dependencies import get_db, get_current_user, require_roles
from ..schemas import TaskRead, TaskUpdate, TaskFilters, GetAllTasksResponse
from ..services import task_service

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("/create", response_model=TaskRead, summary="Create new task", description="Create new task by adding details like task_name, task_description, task_status, user_id ( user_id can only be used by system admin, for users it will result in error being thrown )", dependencies=[Depends(require_roles(UserRoles.ADMIN, UserRoles.USER))])
async def create_task(task_name: str, task_status: TaskStatus, db: AsyncSession= Depends(get_db), current_user = Depends(get_current_user), user_id: Optional[UUID]= None, task_description: Optional[str]= None,):
    task = await task_service.create_task(task_name, task_status, db, current_user, user_id, task_description)
    return task

@router.get("/all", response_model=GetAllTasksResponse, summary="Get current user tasks", description="Gets all tasks related to the logged in user", dependencies=[Depends(require_roles(UserRoles.ADMIN, UserRoles.USER))])
async def get_tasks(filters: TaskFilters = Depends(), page: Annotated[int, Query(ge=1, le=250)] = 1, page_size: Annotated[int, Query(ge=1, le=1000)] = 5, db: AsyncSession = Depends(get_db), user = Depends(get_current_user)):
    tasks = await task_service.get_all_tasks_by_user(filters, user.user_id, page, page_size, db)
    return tasks

@router.get("/user/{user_id}", response_model=List[TaskRead], summary="Gets tasks by user_id", description="Gets all tasks from tasks table linked with user_id ( Admin Accessible only )", dependencies=[Depends(require_roles(UserRoles.ADMIN))])
async def get_tasks_by_user(user_id: UUID, page: Annotated[int, Query(ge=1, le=250)] = 1, page_size: Annotated[int, Query(ge=1, le=1000)] = 5, db: AsyncSession = Depends(get_db), filters: TaskFilters = Depends() ):
    tasks = await task_service.get_all_tasks_by_user(filters, user_id, page, page_size, db)
    return tasks

@router.get("/{task_id}", response_model=TaskRead, summary="Get specific task", description="Gets the specific task linked with task_id")
async def get_task(task_id: UUID, db: AsyncSession= Depends(get_db), user = Depends(get_current_user)):
    task = await task_service.get_task(task_id, db, user)
    return task

@router.patch("/{task_id}", response_model=TaskRead, summary="Update specific task", description="Updates the specific task linked with task_id")
async def edit_task(task_id: UUID, task_details: TaskUpdate, db: AsyncSession= Depends(get_db), user = Depends(get_current_user)):
    task = await task_service.edit_task(task_id, task_details, db, user)
    return task

@router.patch("/deactivate/{task_id}", summary="Deactivates the task", description="Deactivates the provided task")
async def deactivate_task(task_id: UUID, db: AsyncSession= Depends(get_db), user= Depends(get_current_user)):
        await task_service.deactivate_task(task_id, db, user)
        return {"detail": "Task deactivated successfully"}
    
@router.delete("/delete/{task_id}", summary="Deletes the task", description="Deletes the task")
async def delete_task(task_id: UUID, db: AsyncSession= Depends(get_db), user= Depends(get_current_user)):
        await task_service.delete_task(task_id, db, user)
        return {"detail": "Task deleted successfully"}