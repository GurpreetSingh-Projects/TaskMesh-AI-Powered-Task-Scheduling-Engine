from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.features.users.schemas import UserReadRequestSchema, UserCreateRequestSchema
from app.features.users.services import UserService
from uuid import UUID
from pydantic import EmailStr


router = APIRouter(prefix="/users", tags=["users"])

@router.post("/register", response_model= UserReadRequestSchema, summary="New User regsitration related endpoint", description="Creates a new user")
async def create_user( user_details: UserCreateRequestSchema, db: AsyncSession= Depends(get_db)):
    user = await UserService.create_user(user_details.email, db)
    return user

@router.get("/get", response_model=UserReadRequestSchema, summary="Get any user", description="Gets you back the current user details", dependencies=[Depends(require_roles(UserRoles.ADMIN, UserRoles.USER))])
async def get_user(email: EmailStr, db: AsyncSession = Depends(get_db)):
    user = await UserService.get_user_details(email, db)
    return user
        
@router.get("/get", response_model=UserReadRequestSchema, summary="Get any user", description="Gets back you the user, can be done with user_id or email", dependencies=[Depends(require_roles(UserRoles.USER))])
async def get_user(user_id: UUID | None = None, email: EmailStr | None= None, db: AsyncSession = Depends(get_db)):
    pass
    # if not email and not user_id:
    #     raise HTTPException(status_code=400, detail="Please Enter valid details")

    # if user_id:
    #     user = await UserService.get_user_by_id(user_id, db)
    # else:
    #     user = await UserService.get_user_by_email(email, db)
    # return user

# @router.patch("/edit/{user_id}", response_model=UserReadRequestSchema, summary="Edit user details like email", description="Patch endpoint to edit user details like email, password ( Admin Accessible only )", dependencies=[Depends(require_roles(UserRoles.ADMIN, UserRoles.USER))])
# async def edit_user(user_id: UUID, email: EmailStr | None = None, password: str | None = None, db: AsyncSession= Depends(get_db)):
#     # edit_user = await UserService.edit_user(user_id, email, password, db)
#     # return edit_user
#     pass

# @router.patch("/deactivate/{user_id}", summary="Deactivates the current user", description="Deactivates the current user", dependencies=[Depends(require_roles(UserRoles.ADMIN, UserRoles.USER))], dependencies=[Depends(require_roles(UserRoles.ADMIN, UserRoles.USER))])
# async def deactivate_user(user_id: UUID, db: AsyncSession= Depends(get_db)):
#     # await UserService.deactivate_user(user_id, db)
#     # return {"detail": "User deactivated successfully"}
#     pass