from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import EmailStr
from ..core.database import get_db
from ..services.user_service import *
from ..models.users import *

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login")
async def login(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    result = await verifyUser(user_data, db)