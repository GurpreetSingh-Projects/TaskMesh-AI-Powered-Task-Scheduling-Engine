from app.features.onboarding.services import OnboardingService
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.features.users.services import UserService

def get_onboarding_service(db: AsyncSession = Depends(get_db)) -> OnboardingService:
    return OnboardingService(db)