from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.features.users.dependencies import get_user_service
from app.features.users.schemas import UserEditRequestSchema, UserReadResponseSchema
from app.features.users.services import UserService
from uuid import UUID
from pydantic import EmailStr

router = APIRouter(prefix="/users", tags=["Users"])
       
@router.get("/get", response_model= UserReadResponseSchema, summary="Gets the user details", description="Gets back you the user, can be done with user_id or email")
async def get_user(user_id: UUID | None = None, email: EmailStr | None= None, user_services: UserService = Depends(get_user_service)):
    user = await user_services.get_user_details(email=email, user_id=user_id)
    return user

@router.patch("/edit/{user_id}", response_model=UserReadResponseSchema, summary="Edit user details", description="Patch endpoint to edit user details like email, password")
async def edit_user( user_data: UserEditRequestSchema, user_id: UUID, user_services: UserService = Depends(get_user_service)):
    user = await user_services.edit_user(user_data)
    return user
    
@router.patch("/deactivate/{user_id}", summary="Deactivates the current user", description="Deactivates the current user")
async def deactivate_user(user_id: UUID, user_services: UserService = Depends(get_user_service)):
    await user_services.deactivate_user(user_id)
    return {"detail": "User deactivated successfully"}