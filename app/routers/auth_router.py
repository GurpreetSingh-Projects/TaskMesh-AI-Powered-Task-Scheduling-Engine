from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import EmailStr
from ..dependencies.database import get_db
from ..services.user_service import *
from ..models.users import *

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=UserLoginResponse)
async def login(user_data: UserLogin, db: AsyncSession = Depends(get_db)):
    verified_user = await verifyUser(user_data, db)
    
    if not verified_user:
        raise HTTPException(status_code=404, detail="Verification failed")
    
    token = createAccessToken({"sub": str(verified_user.user_id)})
    return {
        "access_token": token,  
        "type": "bearer",
        "user": verified_user
    }