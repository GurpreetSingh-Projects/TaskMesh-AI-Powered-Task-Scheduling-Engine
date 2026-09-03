from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.features.notifications.services import Notifications

def get_notifications_service(db: AsyncSession = Depends(get_db)) -> Notifications:
    return Notifications(db)