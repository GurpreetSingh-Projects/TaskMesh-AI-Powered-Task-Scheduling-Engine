from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from ..models import *
from ..schemas import *
from ..services import *
from ..core.database import get_db

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("/create", response_model=TaskRead)
async def create_task(task_details: TaskCreate, db: AsyncSession= Depends(get_db)):
    task = await createTask(task_details, db)
    return task

@router.get("", response_model=List[TaskRead])
async def get_tasks(db: AsyncSession = Depends(get_db)):
    tasks = await getAllTasks(db)
    return tasks

@router.get("/{user_id}", response_model=List[TaskRead])
async def get_tasks_by_user(user_id: int, db: AsyncSession = Depends(get_db)):
    tasks = await getAllTasksByUser(user_id, db)
    return tasks

@router.get("/{task_id}", response_model=TaskRead)
async def get_task(task_id: int, db: AsyncSession= Depends(get_db)):
    task = await getTask(task_id, db)
    return task

@router.patch("/{task_id}", response_model=TaskRead)
async def edit_task(task_id: int, task_details: TaskUpdate, db: AsyncSession= Depends(get_db)):
    task = await editTask(task_id, task_details, db)
    return task

@router.delete("/delete/{task_id}")
async def delete_task(task_id:int, db: AsyncSession= Depends(get_db)):
        await deleteTask(task_id, db)
        return {"detail": "Task deleted successfully"}