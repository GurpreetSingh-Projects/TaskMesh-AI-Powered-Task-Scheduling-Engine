from fastapi import APIRouter, Depends, File, Form, HTTPException, Query, UploadFile
from pydantic import EmailStr

from app.core.dependencies import require_roles
from app.features.users.dependencies import get_user_service
from app.features.users.enums import UserRoles
from app.features.users.schemas import (
    UserEditRequestSchema,
    UserReadResponseSchema,
    UserSettingsCreateRequestSchema,
    UserSettingsEditRequestSchema,
    UserSettingsReadResponseSchema,
)
from app.features.users.services import UserService

user_router = APIRouter(
    prefix="/users",
    tags=["Users"],
    dependencies=[Depends(require_roles([UserRoles.ADMIN, UserRoles.USER]))],
)

user_settings_router = APIRouter(prefix="/users/settings", tags=["User Settings"])


@user_router.get(
    "/get",
    response_model=UserReadResponseSchema,
    summary="Gets the user details",
    description="Gets back the current user details",
)
async def get_user(
    user=Depends(require_roles([UserRoles.ADMIN, UserRoles.USER])),
    user_service: UserService = Depends(get_user_service),
):
    user = await user_service.get_user_details(user_id=user.user_id)

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
    user=Depends(require_roles([UserRoles.ADMIN, UserRoles.USER])),
    user_service: UserService = Depends(get_user_service),
):
    user_data = UserEditRequestSchema(
        email=email,
        password=password,
        full_name=full_name,
    )

    return await user_service.edit_user(
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
    user=Depends(require_roles([UserRoles.ADMIN, UserRoles.USER])),
    user_service: UserService = Depends(get_user_service),
):
    return await user_service.create_user_settings(
        user=user,
        settings_data=settings_data,
    )


@user_settings_router.get(
    "",
    status_code=201,
    response_model=UserSettingsReadResponseSchema,
    summary="Get user settings",
)
async def get_user_settings(
    user=Depends(require_roles([UserRoles.ADMIN, UserRoles.USER])),
    user_service: UserService = Depends(get_user_service),
):
    return await user_service.get_user_settings(user_id=user.user_id)


@user_settings_router.patch(
    "",
    response_model=UserSettingsReadResponseSchema,
    summary="Update user settings",
)
async def update_user_settings(
    settings_data: UserSettingsEditRequestSchema,
    user=Depends(require_roles([UserRoles.ADMIN, UserRoles.USER])),
    user_service: UserService = Depends(get_user_service),
):
    return await user_service.update_user_settings(
        user=user,
        settings_data=settings_data,
    )


@user_settings_router.patch(
    "/deactivate",
    status_code=204,
    summary="Deactivate user settings",
    description="Admin-only endpoint. Regular users are not authorized to access this endpoint.",
)
async def deactivate_user_settings(
    user=Depends(require_roles([UserRoles.ADMIN])),
    user_service: UserService = Depends(get_user_service),
):
    await user_service.deactivate_user_settings(user=user)
