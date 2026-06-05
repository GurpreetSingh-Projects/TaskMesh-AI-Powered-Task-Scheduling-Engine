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
    
    return await loginUser(response, email, password, db )
    
@router.post("/me", response_model=UserRead)
async def who_am_I(current_user = Depends(getCurrentUser)):
    return current_user

@router.post("/verify-token")
async def verify_token(current_user: User = Depends(getCurrentUser)):
    return {
            "token": "valid",
             "user_id": current_user.user_id
        }
        
@router.post("/refresh-token")
async def refresh_token(request: Request):
    return await refreshUserToken(request)

@router.post("/change-password")
async def change_password(old_password: str,new_password: str, db: AsyncSession= Depends(get_db), user = Depends(getCurrentUser)):
    return await changePassword(old_password, new_password, db, user)

@router.get("/logout", dependencies=[Depends(getCurrentUser)])
async def logout(response: Response):
    return await logoutUser(response)