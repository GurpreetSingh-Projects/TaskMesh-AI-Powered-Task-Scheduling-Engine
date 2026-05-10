from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
from ..schemas.user import *
from ..models.users import *
from ..core.security import *

async def createUser(user_data: UserCreate, db: AsyncSession)-> User:
    new_user=User(
            email= user_data.email,
            hashed_pswd= hashPassword(user_data.password)
            )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

async def getUser(user_id: Optional[int] | None, email: Optional[EmailStr] | None, db:AsyncSession):
    if not email and not user_id:
        raise HTTPException(status_code=404, detail="Please Enter valid details")
    
    if not user_id:
        user_id= (await db.execute(select(User.user_id).where(User.email == email))).scalar_one_or_none()
        
    user = await db.get(User, user_id)
    
    if not user: 
        raise HTTPException(status_code=404, detail="User not found")
    return user

# async def verifyUser(user_data: UserCreate, db:AsyncSession):
#     user = await getUser(user_data.email) # type: ignore
    
#     if not user: 
#         raise HTTPException(status_code=404, detail="User not found")
    
#     password_matched = verifyPassowrd(user_data.password,user.hashed_pswd )
    
#     if not password_matched:
#         return
#     return user


async def getAllUsers(db:AsyncSession):
    result= await db.execute(select(User))
    return result.scalars().all()

async def editUser(user_id: int, email: EmailStr | None, password: str| None, db: AsyncSession):
    user = await getUser(user_id, db)
      
    if email:
        user.email=email
        
    if password:
        user.hashed_pswd = password
        
    await db.commit()
    await db.refresh(user)
    return user

async def deleteUser(user_id: int, db: AsyncSession):
    user = await getUser(user_id, db)
    
    await db.delete(user)
    await db.commit()
    return
    
    