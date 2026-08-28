from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.features.users.schemas import UserReadResponseSchema, UserRequestSchema, UserCreateRequestSchema
from app.features.users.services import UserService
from typing import Annotated
from pydantic import EmailStr
from uuid import UUID

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/get", response_model=UserReadResponseSchema, summary="Get any user", description="Gets you back the current user details", dependencies=[Depends(require_roles(UserRoles.ADMIN, UserRoles.USER))])
async def get_user(email: EmailStr, db: AsyncSession = Depends(get_db)):
    user = await UserService.get_user_details(email, db)
    return user

@router.patch("/edit/{user_id}", response_model=UserReadResponseSchema, summary="Edit user details like email", description="Patch endpoint to edit user details like email, password ( Admin Accessible only )", dependencies=[Depends(require_roles(UserRoles.ADMIN, UserRoles.USER))])
async def edit_user(user_id: UUID, email: EmailStr | None = None, password: str | None = None, db: AsyncSession= Depends(get_db)):
    # edit_user = await UserService.edit_user(user_id, email, password, db)
    # return edit_user
    pass

@router.patch("/deactivate/{user_id}",  summary="Deactivates the current user", description="Deactivates the current user")
async def deactivate_user(user_id: UUID, db: AsyncSession= Depends(get_db)):
    # await UserService.deactivate_user(user_id, db)
    # return {"detail": "User deactivated successfully"}
    pass