from backend.v1.app.routers.auth_router import refresh_token
from fastapi import APIRouter, Depends, AsyncSession, HTTPException, Query
from app.database import get_db
from app.features.users.schemas import UserCreateRequestSchema, UserReadRequestSchema, UserLoginRequestSchema
from app.features.users.services import UserService
from app.features.auth.services import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model= UserReadRequestSchema, summary="New User regsitration", description="Creates a new user")
async def create_user( user_details: UserCreateRequestSchema, db: AsyncSession= Depends(get_db)):
    user = await UserService.create_user(user_details.email, db)
    access_token = AuthService.create_access_token(user)
    refresh_token = AuthService.create_refresh_token(user)
    
    return {
        "message": "User created successfully",
        "user": user,
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.post("/login", response_model= UserReadRequestSchema, summary="New User regsitration related endpoint", description="Creates a new user")
async def create_user( user_details: UserLoginRequestSchema, db: AsyncSession= Depends(get_db)):
    pass

@router.post("/refresh", response_model= UserReadRequestSchema, summary="New User regsitration related endpoint", description="Creates a new user")
async def create_user( user_details: UserLoginRequestSchema, db: AsyncSession= Depends(get_db)):
    pass