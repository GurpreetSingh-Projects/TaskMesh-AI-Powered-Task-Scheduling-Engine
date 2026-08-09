from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.features.users.schemas import UserCreateRequestSchema, UserLoginRequestSchema, UserLoginResponseSchema, UserRegisterResponseSchema
from app.features.users.services import UserService
from app.features.auth.services import AuthService
from app.features.auth.dependencies import get_auth_service

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model= UserRegisterResponseSchema, summary="New User regsitration", description="Creates a new user")
async def create_user( user_details: UserCreateRequestSchema, auth_service: AuthService = Depends(get_auth_service)):
    user = await auth_service.create_user(user_details)
    return user

@router.post("/login", response_model= UserLoginResponseSchema, summary="Existing User login endpoint", description="Authenticates an existing user")
async def login_user( user_details: UserLoginRequestSchema, auth_service: AuthService = Depends(get_auth_service)):
    user = await auth_service.login_user(user_details)
    return user

@router.post("/refresh", response_model= UserLoginResponseSchema, summary="Refresh User token", description="Refreshes user token")
async def refresh_token(refresh_token: str, auth_service: AuthService = Depends(get_auth_service)):
    user = await auth_service.refresh_token(refresh_token)
    return user