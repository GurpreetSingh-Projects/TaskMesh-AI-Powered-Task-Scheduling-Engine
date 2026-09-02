from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.features.activity.services import ActivityService

def get_activity_service(db: AsyncSession = Depends(get_db)) -> ActivityService:
    return ActivityService(db)