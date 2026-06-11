from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from pydantic import EmailStr
from uuid import UUID
from ..models import *
from ..schemas import *
from ..services import *
from ..dependencies import *

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/create", response_model=UserRead, summary="Create a new user", description="Creates a new user")
async def create_user(user_details: UserCreate, db: AsyncSession= Depends(get_db)):
        
        new_user = await createUser(user_details, db)
        return new_user

@router.get("/get", response_model=UserRead, summary="Get any user", description="Gets back you the user, can be done with user_id or email", dependencies=[Depends(require_roles(UserRoles.ADMIN))],)
async def get_user(user_id: Optional[UUID]= None, email: Optional[EmailStr]= None, db: AsyncSession = Depends(get_db)):
    if not email and not user_id:
        raise HTTPException(status_code=400, detail="Please Enter valid details")

    if user_id:
        user = await getUserById(user_id, db)
    else: 
        user = await getUserByEmail(email, db)      
    return user

@router.get("/get/all", response_model=list[UserRead], summary="Get all users", description="Gets back you the list of all users", dependencies=[Depends(require_roles(UserRoles.ADMIN))])
async def get_users(db: AsyncSession = Depends(get_db)):
    users = await getAllUsers(db)
    return users

@router.patch("/edit/{user_id}", response_model=UserRead, summary="Edit user details like email", description="Patch endpoint to edit user details like email, password ( Admin Accessible only )", dependencies=[Depends(require_roles(UserRoles.ADMIN))])
async def edit_user(user_id: UUID, email: Optional[EmailStr]= None, password: Optional[str]= None, db: AsyncSession= Depends(get_db)):
        edit_user = await editUser(user_id, email, password, db)
        return edit_user
    
@router.delete("/delete/{user_id}", summary="Deletes the user", description="Deletes the user along with its linked tasks", dependencies=[Depends(require_roles(UserRoles.ADMIN))])
async def delete_user(user_id: UUID, db: AsyncSession= Depends(get_db)):
        await deleteUser(user_id, db)
        return {"detail": "User deleted successfully"}
