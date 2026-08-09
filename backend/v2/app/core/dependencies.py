from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db

async def get_current_user(auth_service: AuthService = Depends(get_auth_service)) -> User:
    return await auth_service.get_current_user()