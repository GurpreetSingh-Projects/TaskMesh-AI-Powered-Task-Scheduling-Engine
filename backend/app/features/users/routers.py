from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, Form, File

from pydantic import EmailStr

from app.features.users.dependencies import get_user_service
from app.features.users.schemas import UserEditRequestSchema, UserReadResponseSchema, UserSettingsCreateRequestSchema, UserSettingsReadResponseSchema, UserSettingsEditRequestSchema
from app.features.users.services import UserService
from app.core.dependencies import get_current_user

user_router = APIRouter(
    prefix="/users",
    tags=["Users"],
    dependencies=[Depends(get_current_user)],
)

user_settings_router = APIRouter(
    prefix="/users/settings",
    tags=["User Settings"],
    dependencies=[Depends(get_current_user)],
)

@user_router.get(
    "/get",
    response_model=UserReadResponseSchema,
    summary="Gets the user details",
    description="Gets back the current user details",
)
async def get_user(
    user=Depends(get_current_user),
    user_services: UserService = Depends(get_user_service),
):
    user = await user_services.get_user_details(user_id=user.user_id)

    if user.is_deleted and user.deleted_at is not None:
        raise HTTPException(status_code=404, detail="User not found")

    return user

@user_router.patch(
    "/edit",
    response_model=UserReadResponseSchema,
    summary="Edit user details",
    description="Patch endpoint to edit user details like email, password",
)
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

    return await user_services.edit_user(
        user=user,
        user_data=user_data,
        profile_img=profile_img,
    )

@user_settings_router.post(
    "",
    response_model=UserSettingsReadResponseSchema,
    summary="Create user settings",
)
async def create_user_settings(
    settings_data: UserSettingsCreateRequestSchema,
    user=Depends(get_current_user),
    user_services: UserService = Depends(get_user_service),
):
    return await user_services.create_user_settings(
        user=user,
        settings_data=settings_data,
    )

@user_settings_router.get(
    "",
    response_model=UserSettingsReadResponseSchema,
    summary="Get user settings",
)
async def get_user_settings(
    user=Depends(get_current_user),
    user_services: UserService = Depends(get_user_service),
):
    return await user_services.get_user_settings(user=user)

@user_settings_router.patch(
    "",
    response_model=UserSettingsReadResponseSchema,
    summary="Update user settings",
)
async def update_user_settings(
    settings_data: UserSettingsEditRequestSchema,
    user=Depends(get_current_user),
    user_services: UserService = Depends(get_user_service),
):
    return await user_services.update_user_settings(
        user=user,
        settings_data=settings_data,
    )

@user_settings_router.patch(
    "/deactivate",
    status_code=204,
    summary="Deactivate user settings",
)
async def deactivate_user_settings(
    user=Depends(get_current_user),
    user_services: UserService = Depends(get_user_service),
):
    await user_services.deactivate_user_settings(user=user)