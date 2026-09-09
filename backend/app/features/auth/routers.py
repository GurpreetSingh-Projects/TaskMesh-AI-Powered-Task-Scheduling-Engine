from fastapi import APIRouter, Depends, UploadFile, Form, File
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr
from app.database import get_db
from app.features.users.schemas import UserLoginRequestSchema, UserLoginResponseSchema, UserRegisterResponseSchema
from app.features.auth.services import AuthService
from app.features.auth.dependencies import get_auth_service
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model= UserRegisterResponseSchema, status_code=201, summary="New User regsitration", description="Creates a new user")
async def create_user(email:EmailStr= Form(...), password: str= Form(...), profile_img: UploadFile | None = File(None), auth_service: AuthService = Depends(get_auth_service)):
    user = await auth_service.create_user(email=email, password=password,  profile_img= profile_img)
    return user

@router.post("/swagger-login", summary="Endpoint for dev login through swagger docs", description="This endpoint is used for testing purposes in Swagger UI")
async def swagger_login(form_data: OAuth2PasswordRequestForm= Depends(), auth_service: AuthService = Depends(get_auth_service)):
    user_details = UserLoginRequestSchema(
        email= form_data.username,
        password= form_data.password,
    )
    user = await auth_service.login_user(user_details)
    return user

@router.post("/login", response_model= UserLoginResponseSchema, summary="Existing User login endpoint", description="Authenticates an existing user")
async def login_user( user_details: UserLoginRequestSchema, auth_service: AuthService = Depends(get_auth_service)):
    user = await auth_service.login_user(user_details)
    return user

@router.post("/refresh", response_model= UserLoginResponseSchema, summary="Refresh User token", description="Refreshes user token", dependencies=[Depends(get_current_user)])
async def refresh_token(refresh_token: str, auth_service: AuthService = Depends(get_auth_service)):
    user = await auth_service.refresh_token(refresh_token)
    return user

@router.post("/reactivate", status_code=204, summary="Reactivates the current user", description="Reactivates the current user")
async def reactivate_user(user_details: UserLoginRequestSchema, auth_services: AuthService = Depends(get_auth_service)):
    return await auth_services.reactivate_user(user_details)