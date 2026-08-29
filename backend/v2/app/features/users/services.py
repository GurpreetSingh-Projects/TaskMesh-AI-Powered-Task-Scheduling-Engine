from fastapi import HTTPException
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.features.users.schemas import UserCreateRequestSchema
from app.features.users.models import Users

class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user_details(self, user_details: UserCreateRequestSchema):
        query = select(Users).where(Users.email == user_details.email, Users.is_deleted.is_(False))
        user = (await self.db.execute(query)).scalar_one_or_none()
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
