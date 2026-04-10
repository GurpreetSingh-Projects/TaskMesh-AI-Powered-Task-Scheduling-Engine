from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..schemas.user import *
from ..models.users import *

async def createUser(user_data: UserCreate, db: AsyncSession)-> User:
    new_user=User(
            email= user_data.email,
            hashed_pswd= user_data.password
            )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

async def getUser(user_id: int, db:AsyncSession):
    result= await db.execute(select(User).where(User.user_id==user_id))
    return result.scalar_one_or_none()

async def getAllUsers(db:AsyncSession):
    result= await db.execute(select(User))
    return result.scalars().all()