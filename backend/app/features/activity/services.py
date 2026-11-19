from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, insert, update, func
from uuid import UUID
from datetime import datetime, timezone
from loguru import logger
from app.features.users.models import Users
from app.features.activity.models import UserActivity
from app.features.activity.schemas import UserActivityCreateRequestSchema, UserActivityReadResponseSchema

class ActivityService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def record_activity(self, user: Users, activity_data: UserActivityCreateRequestSchema):
        activity_query = (
            insert(UserActivity)
            .values(
                user_id=user.user_id,
                created_by=user.user_id,
                updated_by=user.user_id,
                **activity_data,
            )
            .returning(UserActivity)
        )

        try:
            response = (await self.db.execute(activity_query)).scalar_one_or_none()
        except HTTPException:
            await self.db.rollback()
            raise
        except Exception as e:
            await self.db.rollback()
            raise HTTPException(status_code=500, detail=f"An error occurred while recording activity: {str(e)}")

        return response

    async def create_activity(
        self,
        user: Users,
        activity_data: UserActivityCreateRequestSchema,
    ):
        response= await self.record_activity(user, activity_data)
        return response

    async def get_activities(self, user: Users):
        pass

    async def get_activity(
        self,
        user: Users,
        activity_id: UUID,
    ):
        pass
