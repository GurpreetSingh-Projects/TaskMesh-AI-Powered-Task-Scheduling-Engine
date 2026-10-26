from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.features.labels.services import LabelsService

def get_labels_service(db: AsyncSession = Depends(get_db)) -> LabelsService:
    return LabelsService(db)