from datetime import datetime, timezone
from types import SimpleNamespace
from uuid import UUID

from fastapi import HTTPException, UploadFile
from loguru import logger
from pydantic import EmailStr
from sqlalchemy import and_, or_, select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.core.redis import delete_cache, get_cache, set_cache
from app.core.utils import hash_password
from app.features.activity.enums import ActivityEntityType, UserActivityType
from app.features.activity.schemas import UserActivityCreateRequestSchema
from app.features.activity.services import ActivityService
from app.features.storage.enums import FileStorageEntity
from app.features.storage.models import FileStorage
from app.features.storage.services import StorageService
from app.features.users.models import Users, UserSettings
from app.features.users.schemas import (
    UserEditRequestSchema,
    UserSettingsCreateRequestSchema,
    UserSettingsEditRequestSchema,
    UserSettingsReadResponseSchema,
)


class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.storage_service = StorageService(db)
        self.activity_service = ActivityService(db)

    async def get_user_details(
        self,
        email: EmailStr | None = None,
        user_id: UUID | None = None,
        silent_mode: bool = False,
    ):
        cache_key = ""
        try:
            if not email and not user_id:
                raise HTTPException(
                    status_code=400, detail="Either email or user_id must be provided"
                )

            conditions = []
            if user_id:
                conditions.append(Users.user_id == user_id)
                cache_key = f"users:{user_id}:get"
            if email:
                conditions.append(Users.email == email)

            cached_details = await get_cache(cache_key)

            if user_id is not None and cached_details:
                return SimpleNamespace(**cached_details)

            query = (
                select(
                    Users.user_id,
                    Users.full_name,
                    Users.email,
                    Users.profile_img,
                    Users.hashed_pswd,
                    Users.role,
                    Users.is_profile_completed,
                    Users.is_onboarding_completed,
                    Users.is_deleted,
                    Users.deleted_at,
                    Users.created_by,
                    Users.updated_by,
                    Users.created_at,
                    Users.updated_at,
                    Users.version_number,
                    FileStorage.storage_key,
                )
                .outerjoin(
                    FileStorage,
                    and_(
                        Users.profile_img == FileStorage.file_storage_id,
                        Users.user_id == FileStorage.entity_id,
                        FileStorage.entity_type == FileStorageEntity.PROFILE_IMG,
                    ),
                )
                .where(*conditions)
                .limit(1)
            )

            logger.debug("Redis Cache MISS: Fetching user details from database")

            user = (await self.db.execute(query)).mappings().one_or_none()

            if not user:
                if not silent_mode:
                    raise HTTPException(status_code=404, detail="User not found")
                return None

            user_settings = await self.get_user_settings(user_id=user.user_id)

            user = SimpleNamespace(**user)

            if user.storage_key:
                user.profile_img = await self.storage_service.get_signed_asset_url(
                    user.storage_key
                )

            user.user_settings = UserSettingsReadResponseSchema.model_validate(
                user_settings
            ).model_dump()

            user_data = vars(user)

            await set_cache(cache_key=cache_key, data=user_data)

            return user
        except HTTPException:
            raise
        except Exception:
            logger.exception(f"Failed to retrieve user details:")
            raise

    async def edit_user(
        self,
        user: Users,
        user_data: UserEditRequestSchema | None = None,
        profile_img: UploadFile | None = None,
    ):
        file_record = None
        cache_key = f"users:{user.user_id}:get"

        if user_data is not None:
            user_data = user_data.model_dump(exclude_unset=True, exclude_none=True)

        if not user_data and not profile_img:
            raise HTTPException(
                status_code=400, detail="Invalid update user details provided"
            )

        if profile_img is not None:
            file_record = await self.storage_service.upload_file(
                user=user,
                file=profile_img,
                entity_type=FileStorageEntity.PROFILE_IMG,
                entity_id=str(user.user_id),
            )
            user_data["profile_img"] = str(file_record["item"].file_storage_id)

        password = user_data.pop("password", None)

        if password is not None:
            user_data["hashed_pswd"] = hash_password(password)

        user_data["is_profile_completed"] = bool(
            user.profile_img
            and user.is_onboarding_completed
            and user.email
            and user.full_name
        )

        user_data["updated_by"] = user.user_id

        update_query = (
            update(Users)
            .where(Users.user_id == user.user_id, Users.is_deleted.is_(False))
            .values(**user_data)
            .returning(Users)
        )

        try:
            updated_user = (await self.db.execute(update_query)).scalar_one_or_none()
            if updated_user is None:
                raise HTTPException(
                    status_code=400, detail="No user found with the given id"
                )

            updated_user.user_settings = await self.get_user_settings(
                user_id=user.user_id
            )

            await self.activity_service.record_activity(
                activity_data=UserActivityCreateRequestSchema(
                    activity_type=UserActivityType.PROFILE_UPDATED,
                    entity_type=ActivityEntityType.USERS,
                    entity_id=user.user_id,
                ),
                user=user,
            )
        except HTTPException:
            await self.db.rollback()
            raise
        except IntegrityError as e:
            await self.db.rollback()
            logger.exception(
                "Edit user failed user_id={} err={}", user.user_id, type(e).__name__
            )
            raise HTTPException(
                status_code=409,
                detail="User details conflict with existing records",
            )
        except Exception as e:
            await self.db.rollback()
            logger.exception(
                "Edit user failed user_id={} err={}", user.user_id, type(e).__name__
            )
            raise HTTPException(
                status_code=500,
                detail="An error occurred while updating user!!",
            )

        self.db.expunge(updated_user)

        if updated_user.profile_img:
            file_details = await self.storage_service.get_file_details(
                file_storage_id=updated_user.profile_img,
                entity_type=FileStorageEntity.PROFILE_IMG,
            )
            updated_user.profile_img = await self.storage_service.get_signed_asset_url(
                file_details.storage_key
            )
        else:
            updated_user.profile_img = ""

        await set_cache(cache_key=cache_key, data=user_data)

        await self.db.commit()
        return updated_user

    async def deactivate_user(self, user: Users):
        deactivate_query = (
            update(Users)
            .where(Users.user_id == user.user_id)
            .values(
                is_deleted=True,
                deleted_at=datetime.now(timezone.utc),
                updated_by=user.user_id,
            )
            .returning(Users)
        )

        try:
            response = (await self.db.execute(deactivate_query)).scalar_one_or_none()
            if response is None:
                raise HTTPException(
                    status_code=400, detail="No task found with the given id"
                )
        except HTTPException:
            await self.db.rollback()
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"An error occurred while updating task: {str(e)}",
            )

        cache_key = f"users:{user.user_id}:get"
        await delete_cache(cache_key)

        await self.db.commit()
        return

    async def create_user_settings(
        self,
        user: Users,
        settings_data: UserSettingsCreateRequestSchema,
    ):
        settings_data = settings_data.model_dump(exclude_unset=True)

        if not settings_data:
            raise HTTPException(
                status_code=400, detail="Invalid settings details provided"
            )

        cache_key = f"users:settings:{user.user_id}:get"

        insert_query = (
            insert(UserSettings)
            .values(
                user_id=user.user_id,
                created_by=user.user_id,
                updated_by=user.user_id,
                **settings_data,
            )
            .returning(UserSettings)
        )

        try:
            user_settings = (await self.db.execute(insert_query)).scalar_one_or_none()

            await self.activity_service.record_activity(
                activity_data=UserActivityCreateRequestSchema(
                    activity_type=UserActivityType.SETTINGS_CREATED,
                    entity_type=ActivityEntityType.USERS,
                    entity_id=user.user_id,
                ),
                user=user,
            )

        except HTTPException:
            await self.db.rollback()
            raise
        except IntegrityError:
            await self.db.rollback()
            updated_settings = await self.update_user_settings(
                user=user, settings_data=settings_data
            )

            logger.info(
                "Integrity error while creating settings, updating existing user settings {}"
            )
            await set_cache(cache_key=cache_key, data=user_settings)
            await self.db.commit()

            return updated_settings

        except Exception:
            await self.db.rollback()
            logger.exception("Error while creating user settings {}")
            raise HTTPException(
                status_code=500, detail="An error occurred while creating user settings"
            )

        await set_cache(cache_key=cache_key, data=user_settings)
        await self.db.commit()
        return user_settings

    async def get_user_settings(self, user_id: UUID):
        cache_key = f"users:settings:{user_id}:get"
        cached_data = await get_cache(cache_key=cache_key)

        if cached_data:
            return cached_data

        query = (
            select(UserSettings)
            .where(
                UserSettings.is_deleted.is_(False),
                or_(
                    UserSettings.user_id == user_id,
                    UserSettings.user_id.is_(None),
                ),
            )
            .order_by(UserSettings.user_id.is_(None))
            .limit(1)
        )

        try:
            user_settings = (await self.db.execute(query)).scalars().first()

            if user_settings is None:
                raise HTTPException(status_code=404, detail="User settings not found")

        except HTTPException:
            raise
        except Exception:
            logger.exception("Error while getting user settings")
            raise HTTPException(
                status_code=500, detail="An error occurred while getting user settings"
            )

        await set_cache(cache_key=cache_key, data=user_settings)
        return user_settings

    async def update_user_settings(
        self,
        user: Users,
        settings_data: UserSettingsEditRequestSchema,
    ):
        settings = (
            settings_data
            if isinstance(settings_data, dict)
            else settings_data.model_dump(exclude_unset=True, exclude_none=True)
        )

        if not settings:
            raise HTTPException(
                status_code=400, detail="Invalid settings details provided"
            )

        cache_key = f"users:settings:{user.user_id}:get"

        update_query = (
            update(UserSettings)
            .where(
                UserSettings.user_id == user.user_id,
                UserSettings.is_deleted.is_(False),
            )
            .values(
                **settings,
                updated_by=user.user_id,
            )
            .returning(UserSettings)
        )

        try:
            user_settings = (await self.db.execute(update_query)).scalar_one_or_none()

            if user_settings is None:
                logger.info("Creating new user settings for user: {}", user.user_id)
                settings = await self.create_user_settings(
                    user=user,
                    settings_data=settings_data,
                )

                await self.activity_service.record_activity(
                    activity_data=UserActivityCreateRequestSchema(
                        activity_type=UserActivityType.SETTINGS_CREATED,
                        entity_type=ActivityEntityType.USERS,
                        entity_id=user.user_id,
                    ),
                    user=user,
                )

                return settings

            await self.activity_service.record_activity(
                activity_data=UserActivityCreateRequestSchema(
                    activity_type=UserActivityType.SETTINGS_UPDATED,
                    entity_type=ActivityEntityType.USERS,
                    entity_id=user.user_id,
                ),
                user=user,
            )

        except HTTPException:
            await self.db.rollback()
            raise
        except IntegrityError:
            await self.db.rollback()
            logger.exception("Integrity error while updating user settings: {}")
            raise HTTPException(
                status_code=409, detail="An error occurred while updating user settings"
            )
        except Exception:
            await self.db.rollback()
            logger.exception("Error while updating user settings: {}")
            raise HTTPException(
                status_code=500, detail="An error occurred while updating user settings"
            )

        await set_cache(cache_key=cache_key, data=user_settings)
        await self.db.commit()
        return user_settings

    async def deactivate_user_settings(self, user: Users):
        deleted_at = datetime.now(timezone.utc)
        cache_key = f"users:settings:{user.user_id}:get"

        deactivate_query = (
            update(UserSettings)
            .where(
                UserSettings.user_id == user.user_id,
                UserSettings.is_deleted.is_(False),
            )
            .values(
                is_deleted=True,
                deleted_at=deleted_at,
                updated_by=user.user_id,
            )
            .returning(UserSettings)
        )

        try:
            user_settings = (
                await self.db.execute(deactivate_query)
            ).scalar_one_or_none()

            if user_settings is None:
                raise HTTPException(status_code=404, detail="User settings not found")

        except HTTPException:
            await self.db.rollback()
            raise
        except IntegrityError:
            await self.db.rollback()
            logger.exception("Integrity error while deactivating user settings")
            raise HTTPException(
                status_code=409,
                detail="An error occurred while deactivating user settings",
            )
        except Exception:
            await self.db.rollback()
            logger.exception("Error while deactivating user settings")
            raise HTTPException(
                status_code=500,
                detail="An error occurred while deactivating user settings",
            )

        delete_cache(cache_key)
        await self.db.commit()
        logger.info("Deactivated user settings for user: {}", user.user_id)
        return
