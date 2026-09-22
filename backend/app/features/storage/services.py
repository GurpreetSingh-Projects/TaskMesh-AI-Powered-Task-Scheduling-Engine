import hashlib
import aioboto3
from fastapi import HTTPException, UploadFile
from uuid import UUID
from sqlalchemy import select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timezone
from botocore.config import Config
from app.features.storage.schemas import FileReadResponseSchema
from app.features.storage.enums import FileStorageEntity
from app.features.storage.models import FileStorage
from app.config import settings
import uuid

class StorageService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self._session = aioboto3.Session()
        self._client_kwargs = dict(
            service_name= "s3",
            endpoint_url= settings.B2_ENDPOINT,
            aws_access_key_id= settings.B2_KEY_ID,
            aws_secret_access_key= settings.B2_APPLICATION_KEY,
            config=Config(signature_version="s3v4"),
        )
        self.bucket = settings.B2_BUCKET_NAME

    async def upload_file(self, user, file: UploadFile, entity_type: FileStorageEntity, entity_id: str) -> FileStorage:
        entity_type = entity_type or FileStorageEntity.OTHER
        entity_id = entity_id or uuid.uuid4()

        if file.content_type not in settings.ALLOWED_CONTENT_TYPES:
            raise HTTPException(status_code=400, detail=("Unsupported file type. " f"Supported file formats: {', '.join(settings.ALLOWED_CONTENT_TYPES)}"
            ),
        )
        
        file_bytes = await file.read()
        if len(file_bytes) > settings.MAX_FILE_SIZE:
            raise HTTPException(status_code=400, detail="File too large")

        md5_checksum = hashlib.md5(file_bytes).hexdigest()

        existing_query = (
            select(FileStorage)
            .where(
                FileStorage.md5_checksum == md5_checksum
            )
            .limit(1)
        )

        existing_file = (await self.db.execute(existing_query)).scalar_one_or_none()

        if existing_file:
            if not existing_file.is_deleted:
                return {
                    "item": existing_file,
                    "detail": "Existing file uploaded, returning the existing file details",
                }
            await self.reactivate_file(user=user, file_storage_id=existing_file.file_storage_id)

        storage_key = f"{settings.B2_BUCKET_NAME}/{uuid.uuid4()}"

        try:
            async with self._session.client(**self._client_kwargs) as s3:
                await s3.put_object(
                    Bucket=self.bucket, 
                    Key=storage_key, 
                    Body=file_bytes, 
                    ContentType=file.content_type
                )
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=502,
                detail=f"File upload failed: {str(e)}",
            )

        insert_query = (
            insert(FileStorage)
            .values(
                user_id=user.user_id,
                name=file.filename,
                size=len(file_bytes),
                type=file.content_type,
                entity_id=entity_id,
                entity_type=entity_type,
                storage_key=storage_key,
                bucket_name=self.bucket,
                md5_checksum=md5_checksum,
                created_by=user.user_id,
                updated_by=user.user_id,
            )
            .returning(FileStorage)
        )

        try:
            file_record = (await self.db.execute(insert_query)).scalar_one()
        except HTTPException:
            await self.db.rollback()
            raise
        except Exception as e:
            raise HTTPException(
                status_code=502,
                detail=f"File upload failed: {str(e)}",
            )

        await self.db.commit()
        return {
            "item": file_record,
            "detail": "File uploaded successfully"
        }

    async def get_file_details(
        self,
        file_storage_id: str,
        entity_type: FileStorageEntity = None
    ) -> FileStorage:
        
        entity_type = entity_type or FileStorageEntity.OTHER
        query = (
            select(FileStorage)
            .where(
                FileStorage.file_storage_id == file_storage_id,
                FileStorage.entity_type == entity_type,
                FileStorage.is_deleted.is_(False),
                FileStorage.deleted_at.is_(None)
            )
        )

        file = (await self.db.execute(query)).scalar_one_or_none()

        if file is None:
            raise HTTPException(status_code=404, detail="File not found")

        try:
            async with self._session.client(**self._client_kwargs) as s3:
                file.download_url = await s3.generate_presigned_url(
                    "get_object",
                    Params={
                        "Bucket": self.bucket,
                        "Key": file.storage_key,
                    },
                    ExpiresIn=settings.ASSET_TOKEN_EXPIRY_SECONDS,
                )
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=502,
                detail=f"Failed to generate file URL: {str(e)}",
            )
        return file

    async def deactivate_file(self, file_storage_id, user):
        deactivate_query = (
            update(FileStorage)
            .where(
                FileStorage.file_storage_id == file_storage_id,
                FileStorage.is_deleted.is_(False),
            )
            .values(
                is_deleted=True,
                deleted_at=datetime.now(timezone.utc),
                updated_by=user.user_id,
            )
            .returning(FileStorage)
        )

        try:
            response = (await self.db.execute(deactivate_query)).scalar_one_or_none()
            if response is None:
                raise HTTPException(status_code=404, detail="No file found with the given id")
        except HTTPException:
            await self.db.rollback()
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred while updating file: {str(e)}")

        await self.db.commit()
        return

    async def reactivate_file(self, user, file_storage_id: UUID) -> FileStorage:
        reactivate_query = (
            update(FileStorage)
            .where(
                FileStorage.file_storage_id == file_storage_id,
                FileStorage.is_deleted.is_(True)
            )
            .values(
                is_deleted=False,
                deleted_at=None,
                updated_by=user.user_id,
            )
            .returning(FileStorage)
        )

        try:
            reactivated_file = (await self.db.execute(reactivate_query)).scalar_one()
        except HTTPException:
            await self.db.rollback()
            raise
        except Exception as e:
            await self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Failed to reactivate file: {str(e)}")

        await self.db.commit()
        return {
            "item": reactivated_file,
            "detail": "Previously deleted file reactivated",
        }