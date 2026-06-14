from fastapi import APIRouter, Depends, HTTPException, Response, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from ..dependencies import *
from ..services.user_service import *
from ..models.users import *    
from ..core.security import *

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=UserLoginResponse)
async def login(response: Response, form_data: OAuth2PasswordRequestForm = Depends() , db: AsyncSession = Depends(get_db)):
    email = form_data.username
    password = form_data.password
    
    return await login_user(response, email, password, db )
    
@router.post("/who-am-i", response_model=UserRead)
async def who_am_I(current_user = Depends(get_current_user)):
    return current_user

@router.post("/verify-token")
async def verify_token(current_user: User = Depends(get_current_user)):
    return {
            "token": "valid",
             "user_id": current_user.user_id
        }
        
@router.post("/refresh-token")
async def refresh_token(request: Request):
    return await refresh_user_token(request)

@router.post("/change-password")
async def change_password(old_password: str,new_password: str, db: AsyncSession= Depends(get_db), user = Depends(get_current_user)):
    return await change_password(old_password, new_password, db, user)

@router.get("/logout", dependencies=[Depends(get_current_user)])
async def logout(response: Response):
    return await logout_user(response)