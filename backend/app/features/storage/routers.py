from fastapi import APIRouter, Depends, UploadFile, Form, HTTPException, File
from uuid import UUID
from app.core.dependencies import get_current_user
from app.features.storage.dependencies import get_storage_service
from app.features.storage.schemas import FileReadResponseSchema, FileReadResponseItemSchema
from app.features.storage.services import StorageService
from app.features.storage.enums import FileStorageEntity

router = APIRouter(prefix="/storage", tags=["storage"])

@router.post("/upload", response_model=FileReadResponseSchema, summary="Upload a file", description="Uploads a file and associates it with an entity (task, subtask, onboarding_answer, user_avatar)")
async def upload_file(
    file: UploadFile = File(...),
    entity_type: FileStorageEntity = Form(...),
    entity_id: UUID = Form(...),
    user=Depends(get_current_user),
    storage_service: StorageService = Depends(get_storage_service),
):
    file_record = await storage_service.upload_file(user=user, file=file, entity_type=entity_type, entity_id=entity_id)
    return file_record

@router.get("/get/{file_storage_id}", response_model=FileReadResponseItemSchema, summary="Get file details", description="Gets file metadata and a temporary download URL")
async def get_file(file_storage_id: str, storage_service: StorageService = Depends(get_storage_service)):
    file_record = await storage_service.get_file_details(file_storage_id=file_storage_id)
    return file_record

@router.patch("/deactivate/{file_storage_id}", status_code=204, summary="Deactivate a file with its file storage id", description="Deactivates file record without permanently deleting it")
async def delete_file(file_storage_id: str, user=Depends(get_current_user), storage_service: StorageService = Depends(get_storage_service)):
    await storage_service.deactivate_file(file_storage_id=file_storage_id, user=user)
    return