from fastapi import HTTPException, UploadFile
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from uuid import uuid4, UUID
from app.features.users.models import Users
from app.features.labels.models import Labels
from app.features.labels.schemas import LabelCreateSchema
from app.features.storage.services import StorageService
from app.features.storage.enums import FileStorageEntity

class LabelsService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.storage_service = StorageService(db)

    async def create_label(self, user: Users, label_data: LabelCreateSchema, label_img: UploadFile | None = None):
        file_record= None
        label_id= uuid4()

        if label_data is not None: 
            label_data = label_data.model_dump(exclude_unset= True, exclude_none= True)

        if label_img is not None:
            file_record= await self.storage_service.upload_file(
                user=user,
                entity_type=FileStorageEntity.LABEL,
                entity_id=label_id,
            )
            label_data["file_storage_id"]=str(file_record["item"].file_storage_id)
            
        label_data["user_id"]= user.user_id

        insert_query= (
            insert(Labels)
            .values(
                **label_data
            )
            .returning(Labels)
        )

        try:
            response = (await self.db.execute(insert_query)).scalar_one_or_none()
        except HTTPException:
            await self.db.rollback()
            raise
        except IntegrityError as e:
            await self.db.rollback()
            raise HTTPException(status_code = 409, detail=f"Duplicate label detected, addition cancelled!")
        except Exception as e:
            await self.db.rollback()
            raise HTTPException(status_code=500, detail=f"An error occurred while adding label: {str(e)}")
        
        self.db.expunge(response)
        if response.file_storage_id:
            file_details= await self.storage_service.get_file_details(file_storage_id=response.file_storage_id, entity_type=FileStorageEntity.TASK)
            response.image_url= await self.storage_service.get_signed_asset_url(storage_key= file_details.storage_key)
        else:
            response.image_url= None

        await self.db.commit()
        return response
        
    async def get_labels(self, user: uuid.UUID, limit: int = 20, offset: int = 0):
        pass

    async def get_label(self, user: uuid.UUID, label_id: UUID):
        pass

    async def update_label(self, user: uuid.UUID, label_id: UUID, label_data):
        pass