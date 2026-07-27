from fastapi import Depends, HTTPException, Response, Request
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordBearer
from pydantic import EmailStr
from uuid import UUID
from .database import get_db
from ..models import User
from ..core.config import settings
from ..core import security
from ..services import user_service

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    decoded_token = security.decode_token(token)
    
    if decoded_token is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    user_id = decoded_token["sub"]
    user = await user_service.get_user_by_id(UUID(user_id), db)
    return user

async def login_user(response: Response, email: EmailStr, password: str, db: AsyncSession = Depends(get_db)):
    verified_user = await user_service.verify_user(email, password, db)
    
    if not verified_user:
        raise HTTPException(status_code=401, detail="Verification failed")
    
    access_token = security.create_access_token({"sub": str(verified_user.user_id)})
    refresh_token = security.create_refresh_token({"sub": str(verified_user.user_id)})
    
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 3600
    )
    
    return {
        "access_token": access_token,
        "type": "bearer",
        "user": verified_user
    }
    
async def refresh_user_token(request: Request):
    refresh_token = request.cookies.get("refresh_token")
    
    if not refresh_token:
        raise HTTPException(status_code=401, detail="No cookie found!!")
    
    payload = security.decode_token(str(refresh_token))
    
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid cookie found!!")
    
    access_token = security.create_access_token({"sub": str(payload["sub"]) })
    
    return {
            "access_token": access_token,
            "type": "bearer",
        }
    
async def logout_user(response: Response):
    response.delete_cookie("refresh_token")
    return {
        "detail": "Logged out successfully!!"
    }
    
async def change_password(old_password: str, new_password:str, db: AsyncSession, user_data: User):
    user = await user_service.get_user_by_id(user_data.user_id, db)
    response = security.verify_password(old_password, user.hashed_pswd)
        
    if not response:
       raise HTTPException(status_code=400, detail="Unauthorized Access!!")
    
    is_verified = security.verify_password(new_password, user.hashed_pswd)
    
    if is_verified:
       raise HTTPException(status_code=403, detail="Old and new passwords cannot be same")
        
    user.hashed_pswd = security.hash_password(new_password)
    await db.commit()
        
    return {
        "detail": "Your password was updated successfully!!"
    }