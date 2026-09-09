from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.features.tasks.services import TaskService

def get_tasks_service(db: AsyncSession = Depends(get_db)) -> TaskService:
    return TaskService(db)