from fastapi import HTTPException, UploadFile, File
from uuid import UUID
from types import SimpleNamespace
from sqlalchemy import select, update, and_
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from pydantic import EmailStr
from datetime import datetime, timezone
from app.features.users.schemas import UserEditRequestSchema
from app.features.users.models import Users
from app.core.utils import hash_password
from app.features.storage.models import FileStorage
from app.features.storage.enums import FileStorageEntity
from app.features.storage.services import StorageService

class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.storage_service= StorageService(db)

    async def get_user_details(self, email: EmailStr | None = None, user_id: UUID | None = None, silent_mode: bool= False):
        if not email and not user_id:
            raise HTTPException(status_code=400, detail="Either email or user_id must be provided")

        conditions = []
        if user_id:
            conditions.append(Users.user_id == user_id)
        if email:
            conditions.append(Users.email == email)

        query = (
            select(
                Users.user_id,
                Users.full_name,
                Users.email,
                Users.profile_img,
                Users.hashed_pswd,
                Users.role,
                Users.is_onboarding_completed,
                Users.is_deleted,
                Users.deleted_at,
                Users.created_by,
                Users.updated_by,
                Users.created_at,
                Users.updated_at,
                Users.version_number,
                FileStorage.storage_key
            )
            .outerjoin(
                FileStorage,
                and_(
                    Users.profile_img == FileStorage.file_storage_id,
                    Users.user_id == FileStorage.entity_id,
                    FileStorage.entity_type == FileStorageEntity.PROFILE_IMG,
                )
            )
            .where(
                *conditions
            )
            .limit(1)
        )

        user = (await self.db.execute(query)).mappings().one_or_none()

        if not user:
            if not silent_mode:
                raise HTTPException(status_code=404, detail="User not found")
            return None

        user = SimpleNamespace(**user)

        if user.storage_key:
            user.profile_img = await self.storage_service.get_signed_asset_url(user.storage_key)

        return user

    async def edit_user(self, user: Users, user_data: UserEditRequestSchema, profile_img: UploadFile | None = None):
        user_data= user_data.model_dump(exclude_unset= True, exclude_none= True)

        if not user_data and not profile_img:
            raise HTTPException(status_code= 400, detail= "Invalid update user details provided")

        if profile_img is not None:
            file_record = await self.storage_service.upload_file(
                user=user,
                file=profile_img,
                entity_type=FileStorageEntity.PROFILE_IMG,
                entity_id=str(user.user_id),
            )
            user_data["profile_img"]=str(file_record["item"].file_storage_id)

        password = user_data.pop("password", None)

        if password is not None:
            user_data["hashed_pswd"]= hash_password(user_data["password"])
            
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
            updated_user = (await self.db.execute(update_query)).scalar_one_or_none()
            if updated_user is None:
                raise HTTPException(status_code= 400, detail= "No user found with the given id")
        except HTTPException:
            await self.db.rollback()
            raise
        except IntegrityError as e:
            await self.db.rollback()
            raise HTTPException(status_code = 409, detail=f"An error occurred while updating user: {str(e)}")
        except Exception as e:
            await self.db.rollback()
            raise HTTPException(status_code=500, detail=f"An error occurred while updating user: {str(e)}")

        if file_record:
            self.db.expunge(updated_user)
            updated_user.profile_img= await self.storage_service.get_signed_asset_url(file_record["item"].storage_key)

        await self.db.commit()
        return updated_user

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