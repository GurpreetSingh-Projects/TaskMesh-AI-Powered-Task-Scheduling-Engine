from fastapi import HTTPException, UploadFile
from sqlalchemy import insert, select, update, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from uuid import uuid4, UUID
from loguru import logger
from app.features.users.models import Users
from app.features.labels.models import Labels, LabelMapping
from app.features.labels.schemas import LabelCreateSchema
from app.features.storage.services import StorageService
from app.features.storage.enums import FileStorageEntity
from app.features.activity.enums import UserActivityType, ActivityEntityType
from app.features.activity.services import ActivityService
from app.features.activity.schemas import UserActivityCreateRequestSchema
from app.features.labels.enums import LabelOwner

class LabelsService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.storage_service = StorageService(db)
        self.activity_service= ActivityService(db)

    async def create_label(self, user: Users, label_data: LabelCreateSchema, label_img: UploadFile | None = None):
        file_record= None
        label_id= uuid4()

        if label_data is not None: 
            label_data = label_data.model_dump(exclude_unset= True, exclude_none= True)

        entity_type = label_data.pop("entity_type", None)
        entity_id = label_data.pop("entity_id", None)

        if label_img is not None:
            file_record= await self.storage_service.upload_file(
                user=user,
                file= label_img,
                entity_type= FileStorageEntity.LABEL,
                entity_id= str(label_id),
            )
            label_data["file_storage_id"]=str(file_record["item"].file_storage_id)

        label_data["label_id"] = label_id
        label_data["ownership"]= user.role
        label_data["user_id"]= user.user_id

        label_insert_query= (
            insert(Labels)
            .values(
                **label_data
            )
            .returning(Labels)
        )

        try:
            label_response = (await self.db.execute(label_insert_query)).scalar_one_or_none()

            if entity_id is not None and entity_type is not None:
                label_mapping_insert = (
                    insert(LabelMapping)
                    .values(
                        label_id=label_id,
                        entity_type=entity_type,
                        entity_id=entity_id,
                        created_by=user.user_id,
                        updated_by=user.user_id,
                    )
                    .returning(LabelMapping)
                )
                
                label_mapping_response = (await self.db.execute(label_mapping_insert)).scalar_one_or_none()

                await self.activity_service.record_activity(
                        activity_data= UserActivityCreateRequestSchema(
                        activity_type= UserActivityType.LABEL_ADDED,
                        entity_type= ActivityEntityType.LABELS,
                        entity_id= label_id,
                    ),
                    user= user
                )
                
        except HTTPException:
            await self.db.rollback()
            raise

        except IntegrityError as e:
            await self.db.rollback()
            logger.warning("Integrity error on label create | label_id={} user_id={} | {}", label_id, user.user_id, e.orig)
            raise HTTPException(status_code=409, detail="Duplicate label detected, addition cancelled!")

        except Exception:
            await self.db.rollback()
            logger.exception("Label create failed | label_id={} user_id={}", label_id, user.user_id)
            raise
        
        self.db.expunge(label_response)
        if label_response.file_storage_id:
            file_details= await self.storage_service.get_file_details(file_storage_id=label_response.file_storage_id, entity_type=FileStorageEntity.LABEL)
            label_response.image_url= await self.storage_service.get_signed_asset_url(storage_key= file_details.storage_key)
        else:
            label_response.image_url= None

        await self.db.commit()
        logger.info("Label created | label_id={} user_id={}", label_id, user.user_id)
        return label_response

    async def get_labels(self, user: Users, limit: int = 20):
        query= (
                select(Labels)
                .where(
                    Labels.is_deleted.is_(False),
                    or_(
                        Labels.user_id == user.user_id,
                        Labels.ownership == LabelOwner.ADMIN,
                        Labels.ownership == LabelOwner.SYSTEM,
                    )
                )
                .limit(limit)
            )

        labels = (await self.db.execute(query)).scalars().all()

        for label in labels:
            if label.file_storage_id:
                file_details= await self.storage_service.get_file_details(file_storage_id=label.file_storage_id, entity_type=FileStorageEntity.LABEL)
                label.image_url= await self.storage_service.get_signed_asset_url(storage_key= file_details.storage_key)
            else:
                label.image_url= None

            self.db.expunge(label)
        
        return {
            "items": labels,
        }
        
    async def get_label(self, user: Users, label_id: UUID):
        try:
            query = (
                select(Labels)
                .where(
                    Labels.label_id == label_id,
                    Labels.is_deleted.is_(False),
                    or_(
                        Labels.user_id == user.user_id,
                        Labels.ownership.in_([LabelOwner.ADMIN, LabelOwner.SYSTEM]),
                    ),
                )
                .limit(1)
            )
            label = (await self.db.execute(query)).scalar_one_or_none()

            if label is None:
                raise HTTPException(status_code=404, detail="Label not found")

            if label.file_storage_id:
                file_details = await self.storage_service.get_file_details(
                    file_storage_id=label.file_storage_id,
                    entity_type=FileStorageEntity.LABEL,
                )
                label.image_url = await self.storage_service.get_signed_asset_url(
                    storage_key=file_details.storage_key
                )

            self.db.expunge(label)
            return {
                "items": label
            }

        except HTTPException:
            raise
        except Exception as e:
            logger.exception("get_label failed user_id={} label_id={}: {}", user.user_id, label_id, e)
            raise HTTPException(status_code=500, detail="Failed to fetch label")

    # Unused function for updating label, implementation pending due to other p0 tasks
    async def update_label(self, user: Users, label_id: UUID, label_data):
        pass