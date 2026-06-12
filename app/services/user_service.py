from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.dialects.postgresql import insert
from fastapi import HTTPException
from datetime import datetime, timezone
from ..schemas.user_schemas import *
from ..models.users import *
from ..core.security import hashPassword, verifyPassword
import logging

logger = logging.getLogger(__name__)

async def createUser(user_data: UserCreate, db: AsyncSession):    
    query = insert(User).values(
        email= user_data.email,
        hashed_pswd= hashPassword(user_data.password),
        role = UserRoles.USER,
        is_deleted = False
    )

    query = query.on_conflict_do_update(
        index_elements=[User.email],
        set_= {User.is_deleted: False},
        where=(User.is_deleted.is_(True))
    ).returning(User)
    
    try:
        result= (await db.execute(query)).scalar_one_or_none()
        await db.commit()
        return result
    
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=409, detail="User already exists!! please login with your current account")
    
    except Exception:
        await db.rollback()
        logger.exception("Unexpected error occurred during Create User")

async def getUserByEmail(email: EmailStr | None, db: AsyncSession,):
    user= (await db.execute(select(User).where((User.email == email) & (User.is_deleted == False)))).scalar_one_or_none()
    
    if not user: 
        raise HTTPException(status_code=404, detail="User not found")
    return user

async def getUserById(user_id: UUID | None, db: AsyncSession):
    user = (await db.execute(select(User).where((User.user_id == user_id) & (User.is_deleted == False)))).scalar_one_or_none()
    
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

async def editUser(user_id: UUID, email: EmailStr | None, password: str| None, db: AsyncSession):
    user = await getUserById(user_id, db)
      
    if email:
        user.email=email
    if password:
        user.hashed_pswd = hashPassword(password)
    
    user.updated_by = user.user_id
        
    await db.commit()
    await db.refresh(user)
    return user

async def deactivateUser(user_id: UUID, db: AsyncSession):
    user = await getUserById(user_id, db)
    
    user.is_deleted = True
    user.deleted_at = datetime.now(timezone.utc)

    await db.commit()
    return

async def deleteUser(user_id: UUID, db: AsyncSession):
    user = await getUserById(user_id, db)
    
    await db.delete(user)
    await db.commit()
    return