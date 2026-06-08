from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from ..models import *
from ..schemas import *
from ..services import *
from ..dependencies import *

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("/create", response_model=TaskRead, summary="Create new task", description="Create new task by adding details like task_name, task_description, task_status, user_id ( user_id can only be used by system admin, for users it will result in error being thrown )", dependencies=[Depends(require_roles(UserRoles.ADMIN, UserRoles.USER))])
async def create_task(task_name: str, task_status: TaskStatus, db: AsyncSession= Depends(get_db), current_user = Depends(getCurrentUser), user_id: Optional[int]= None, task_description: Optional[str]= None,):
    task = await createTask(task_name, task_status, db, current_user, user_id, task_description)
    return task

@router.get("", response_model=List[TaskRead], summary="Get current user tasks", description="Gets all tasks related to the logged in user", dependencies=[Depends(require_roles(UserRoles.ADMIN, UserRoles.USER))])
async def get_tasks( db: AsyncSession = Depends(get_db), user = Depends(getCurrentUser)):
    tasks = await getAllTasksByUser(user.user_id, db)
    return tasks

@router.get("/user/{user_id}", response_model=List[TaskRead], summary="Gets tasks by user_id", description="Gets all tasks from tasks table linked with user_id", dependencies=[Depends(require_roles(UserRoles.ADMIN))])
async def get_tasks_by_user(user_id: int, db: AsyncSession = Depends(get_db)):
    tasks = await getAllTasksByUser(user_id, db)
    return tasks

@router.get("/{task_id}", response_model=TaskRead, summary="Get specific task", description="Gets the specific task linked with task_id")
async def get_task(task_id: int, db: AsyncSession= Depends(get_db), user = Depends(getCurrentUser)):
    task = await getTask(task_id, db, user)
    return task

@router.patch("/{task_id}", response_model=TaskRead, summary="Update specific task", description="Updates the specific task linked with task_id")
async def edit_task(task_id: int, task_details: TaskUpdate, db: AsyncSession= Depends(get_db), user = Depends(getCurrentUser)):
    task = await editTask(task_id, task_details, db, user)
    return task

@router.delete("/delete/{task_id}", summary="Deletes the task", description="Deletes the task")
async def delete_task(task_id:int, db: AsyncSession= Depends(get_db), user= Depends(getCurrentUser)):
        await deleteTask(task_id, db, user)
        return {"detail": "Task deleted successfully"}