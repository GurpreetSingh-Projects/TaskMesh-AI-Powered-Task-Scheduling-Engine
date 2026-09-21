from fastapi import HTTPException
from uuid import UUID
from sqlalchemy import select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import EmailStr
from datetime import datetime, timezone
from app.features.users.schemas import UserEditRequestSchema
from app.features.users.models import Users
from app.core.utils import hash_password

class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user_details(self, email: EmailStr | None = None, user_id: UUID | None = None):
        if not email and not user_id:
            raise HTTPException(status_code=400, detail="Either email or user_id must be provided")
        elif email and user_id:
            query = select(Users).where(Users.user_id == user_id, Users.email == email, Users.is_deleted.is_(False)).limit(1)
        elif user_id and not email:
            query = select(Users).where(Users.user_id == user_id, Users.is_deleted.is_(False)).limit(1)
        elif not user_id and email:
            query = select(Users).where(Users.email == email, Users.is_deleted.is_(False)).limit(1)
        else:
            raise HTTPException(status_code=400, detail="Invalid request parameters")

        user = (await self.db.execute(query)).scalar_one_or_none()
    
        if not user:
                raise HTTPException(status_code=404, detail="User not found")
        return user


    async def edit_user(self, user: Users, user_data: UserEditRequestSchema):
        user_data= user_data.model_dump(exclude_unset= True)

        if not user_data:
            raise HTTPException(status_code= 400, detail= "Invalid update user details provided")

        user_data["updated_by"]= user.user_id

        update_query= (
            update(Users)
            .where(
                Users.user_id == user.user_id,
                Users.is_deleted.is_(False)
            )
            .values(**user_data)
            .returning(Users)
        )

        try:
            response = (await self.db.execute(update_query)).scalar_one_or_none()
            if response is None:
                raise HTTPException(status_code= 400, detail= "No user found with the given id")
        except HTTPException:
            await self.db.rollback()
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred while updating user: {str(e)}")

        await self.db.commit()
        return response

    async def deactivate_user(self, user_id: UUID):
        deactivate_query= (
            update(Users)
            .where(
                Users.user_id == user_id
            )
            .values(
                is_deleted= True,
                deleted_at= datetime.now(timezone.utc),
                updated_by= user_id
            )
            .returning(Users)
        )

        try:
            response = (await self.db.execute(deactivate_query)).scalar_one_or_none()
            if response is None:
                raise HTTPException(status_code= 400, detail= "No task found with the given id")
        except HTTPException:
            await self.db.rollback()
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred while updating task: {str(e)}")

        await self.db.commit()
        return