from fastapi import Depends, HTTPException, Response, Request
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import EmailStr
from .database import get_db
from ..models import *
from ..core.config import settings
from ..core.security import *
from ..services.user_service import *

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def getCurrentUser(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    decoded_token = decodeToken(token)
    
    if decoded_token is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    user_id = decoded_token["sub"]
    user = await getUserById(int(user_id), db)
    return user

async def loginUser(response: Response, email: EmailStr, password: str, db: AsyncSession = Depends(get_db)):
    verified_user = await verifyUser(email, password, db)
    
    if not verified_user:
        raise HTTPException(status_code=401, detail="Verification failed")
    
    access_token = createAccessToken({"sub": str(verified_user.user_id)})
    refresh_token = createRefreshToken({"sub": str(verified_user.user_id)})
    
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
    
async def refreshUserToken(request: Request):
    refresh_token = request.cookies.get("refresh_token")
    
    if not refresh_token:
        raise HTTPException(status_code=401, detail="No cookie found!!")
    
    payload = decodeToken(str(refresh_token))
    
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid cookie found!!")
    
    access_token = createAccessToken({"sub": str(payload["sub"]) })
    
    return {
            "access_token": access_token,
            "type": "bearer",
        }
    
async def logoutUser(response: Response):
    response.delete_cookie("refresh_token")
    return {
        "detail": "Logged out successfully!!"
    }
    
async def changePassword(old_password: str, new_password:str, db: AsyncSession, user_data: User):
    user = await getUserById(user_data.user_id, db)
    response = verifyPassword(old_password, user.hashed_pswd)
        
    if not response:
       raise HTTPException(status_code=400, detail="Unauthorized Access!!")
    
    if verifyPassword(new_password, user.hashed_pswd):
       raise HTTPException(status_code=403, detail="Old and new passwords cannot be same")
        
    user.hashed_pswd = hashPassword(new_password)
    await db.commit()
        
    return {
        "detail": "Your password was updated successfully!!"
    }