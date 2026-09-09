from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, Form, File
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from pydantic import EmailStr
from app.database import get_db
from app.features.users.dependencies import get_user_service
from app.features.users.schemas import UserEditRequestSchema, UserReadResponseSchema
from app.features.users.services import UserService
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/users", tags=["Users"], dependencies=[Depends(get_current_user)])
       
@router.get("/get", response_model= UserReadResponseSchema, summary="Gets the user details", description="Gets back you the user, can be done with user_id or email")
async def get_user(user= Depends(get_current_user), user_services: UserService = Depends(get_user_service)):
    user = await user_services.get_user_details(user_id=user.user_id)
    if user.is_deleted and user.deleted_at is not None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.patch("/edit", response_model=UserReadResponseSchema, summary="Edit user details", description="Patch endpoint to edit user details like email, password")
async def edit_user(
    email: EmailStr | None = Form(None),
    password: str | None = Form(None),
    full_name: str | None = Form(None),
    profile_img: UploadFile | None = File(None),
    user=Depends(get_current_user),
    user_services: UserService = Depends(get_user_service),
):
    user_data = UserEditRequestSchema(
        email=email,
        password=password,
        full_name=full_name,
    )
    user = await user_services.edit_user(
        user= user, 
        user_data= user_data, 
        profile_img=profile_img
    )
    return user
    
@router.patch("/deactivate", status_code=204, summary="Deactivates the current user", description="Deactivates the current user")
async def deactivate_user(user= Depends(get_current_user), user_services: UserService = Depends(get_user_service)):
    await user_services.deactivate_user(user.user_id)
    return