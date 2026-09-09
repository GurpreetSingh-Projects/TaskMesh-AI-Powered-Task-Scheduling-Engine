from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.features.labels.services import LabelService

def get_label_service(db: AsyncSession = Depends(get_db)) -> LabelService:
    return LabelService(db)