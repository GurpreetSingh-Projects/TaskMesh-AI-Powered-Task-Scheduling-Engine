from fastapi import HTTPException
from uuid import UUID
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.features.users.schemas import UserCreateRequestSchema
from app.features.users.models import Users

class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user_details(self, email: str | None = None, user_id: UUID | None = None):
        if not email and not user_id:
            raise HTTPException(status_code=400, detail="Either email or user_id must be provided")
        
        if user_id:
            query = select(Users).where(Users.user_id == user_id, Users.is_deleted.is_(False))
        elif email is not None:
            query = select(Users).where(Users.email == email, Users.is_deleted.is_(False))

        user = (await self.db.execute(query)).scalar_one_or_none()
    
        if not user:
                raise HTTPException(status_code=404, detail="User not found")
        return user

    # only for reference

    #     async def edit_user(
    #         user_id: UUID,
    #         email: EmailStr | None,
    #         password: str | None,
    #         db: AsyncSession
    #     ):
    #         user = await get_user_by_id(user_id, db)

    #         if email:
    #             user.email = email

    #         if password:
    #             user.hashed_pswd = hash_password(password)

    #         user.updated_by = user.user_id

    #         await db.commit()
    #         await db.refresh(user)
    #         return user


    #     async def deactivate_user(user_id: UUID, db: AsyncSession):
    #         user = await get_user_by_id(user_id, db)

    #         user.is_deleted = True
    #         user.deleted_at = datetime.now(timezone.utc)

    #         await db.commit()
    #         return


    #     async def delete_user(user_id: UUID, db: AsyncSession):
    #         user = await get_user_by_id(user_id, db)

    #         await db.delete(user)
    #         await db.commit()
    #         return
