from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, Annotated
from pydantic import EmailStr
from uuid import UUID
from ..models import UserRoles
from ..schemas import UserRead, UserCreate, GetAllUsersResponse
from ..services import user_service
from ..dependencies import get_db, require_roles

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/register", response_model=UserRead, summary="Create a new user", description="Creates a new user")
async def create_user(user_details: UserCreate, db: AsyncSession= Depends(get_db)):
        
        new_user = await user_service.create_user(user_details, db)
        return new_user

@router.get("/get", response_model=UserRead, summary="Get any user", description="Gets back you the user, can be done with user_id or email", dependencies=[Depends(require_roles(UserRoles.ADMIN))],)
async def get_user(user_id: Optional[UUID]= None, email: Optional[EmailStr]= None, db: AsyncSession = Depends(get_db)):
    if not email and not user_id:
        raise HTTPException(status_code=400, detail="Please Enter valid details")

    if user_id:
        user = await user_service.get_user_by_id(user_id, db)
    else:
        user = await user_service.get_user_by_email(email, db)
    return user

@router.get("/get/all", response_model= GetAllUsersResponse, summary="Get all users", description="Gets back you the list of all users ( Admin Accessible only )", dependencies=[Depends(require_roles(UserRoles.ADMIN))])
async def get_users(page: Annotated[int, Query(ge = 1, le = 999)] = 1, page_size: Annotated[int, Query(ge=1, le=999)] = 5, db: AsyncSession = Depends(get_db)):
    users = await user_service.get_all_users(page, page_size, db)
    return users

@router.patch("/edit/{user_id}", response_model=UserRead, summary="Edit user details like email", description="Patch endpoint to edit user details like email, password ( Admin Accessible only )", dependencies=[Depends(require_roles(UserRoles.ADMIN))])
async def edit_user(user_id: UUID, email: Optional[EmailStr]= None, password: Optional[str]= None, db: AsyncSession= Depends(get_db)):
        edit_user = await user_service.edit_user(user_id, email, password, db)
        return edit_user

@router.patch("/deactivate/{user_id}", summary="Deactivates the current user", description="Deactivates the current user", dependencies=[Depends(require_roles(UserRoles.ADMIN, UserRoles.USER))])
async def deactivate_user(user_id: UUID, db: AsyncSession= Depends(get_db)):
        await user_service.deactivate_user(user_id, db)
        return {"detail": "User deactivated successfully"}
    
@router.delete("/delete/{user_id}", summary="Deletes the user", description="Deletes the user along with its linked tasks ( Admin Accessible only )", dependencies=[Depends(require_roles(UserRoles.ADMIN))])
async def delete_user(user_id: UUID, db: AsyncSession= Depends(get_db)):
        await user_service.delete_user(user_id, db)
        return {"detail": "User deleted successfully"}