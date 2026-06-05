from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
from ..schemas.user_schemas import *
from ..models.users import *
from ..core.security import hashPassword, verifyPassword

async def createUser(user_data: UserCreate, db: AsyncSession)-> User:
    existing_user = (await db.execute(select(User).where(User.email == user_data.email))).scalar_one_or_none()
    
    if existing_user :
        raise HTTPException(status_code=409, detail="User already exists!! please try with different email")
    
    new_user=User(
            email= user_data.email,
            hashed_pswd= hashPassword(user_data.password)
            )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

async def getUserByEmail(email: EmailStr | None, db: AsyncSession,):
    user= (await db.execute(select(User).where(User.email == email))).scalar_one_or_none()
    
    if not user: 
        raise HTTPException(status_code=404, detail="User not found")
    return user

async def getUserById(user_id: int, db: AsyncSession):
    user = await db.get(User, user_id)
    
    if not user: 
        raise HTTPException(status_code=404, detail="User not found")
    return user

async def verifyUser(email: EmailStr, password: str, db:AsyncSession):
    user = await getUserByEmail(email, db)
    
    if not user: 
        raise HTTPException(status_code=401, detail="Invalid Credentials!!")
    
    password_matched = verifyPassword(password, user.hashed_pswd )
    
    if not password_matched:
        raise HTTPException(status_code=401, detail="Invalid Credentials!!")

    return user

async def getAllUsers(db:AsyncSession):
    result= await db.execute(select(User))
    return result.scalars().all()

async def editUser(user_id: int, email: EmailStr | None, password: str| None, db: AsyncSession):
    user = await getUserById(user_id, db)
      
    if email:
        user.email=email
        
    if password:
        user.hashed_pswd = hashPassword(password)
        
    await db.commit()
    await db.refresh(user)
    return user

async def deleteUser(user_id: int, db: AsyncSession):
    user = await getUserById(user_id, db)
    
    await db.delete(user)
    await db.commit()
    return