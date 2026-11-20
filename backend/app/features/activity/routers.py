from fastapi import APIRouter, Depends, UploadFile, Form, File, Query
from uuid import UUID
from app.core.dependencies import get_current_user
from app.features.activity.dependencies import get_activity_service
from app.features.activity.enums import UserActivityType
from app.features.activity.services import ActivityService
from app.features.activity.schemas import UserActivityCreateRequestSchema, UserActivityReadResponseSchema


router= APIRouter(prefix="/activity", tags=["Activity"], dependencies=[Depends(get_current_user)])

@router.post("", response_model=UserActivityReadResponseSchema)
async def create_activity(
    activity_type: UserActivityType,
    user_device_id: str | None = None,
    entity_type: str | None = None,
    entity_id: UUID | None = None,
    user=Depends(get_current_user),
    activity_service: ActivityService = Depends(get_activity_service),
):
    activity_data = UserActivityCreateRequestSchema(
        activity_type= activity_type,
        user_device_id= user_device_id,
        entity_type= entity_type,
        entity_id= entity_id,
    )
    return await activity_service.create_activity(user, activity_data)

@router.get("", response_model=list[UserActivityReadResponseSchema])
async def get_activities(
    user=Depends(get_current_user),
    limit: int = Query(default= 10, gt=0, le= 100),
    activity_service: ActivityService = Depends(get_activity_service),
):
    return await activity_service.get_activities(user)

@router.get("/{activity_id}", response_model=UserActivityReadResponseSchema)
async def get_activity(
    activity_id: UUID,
    user=Depends(get_current_user),
    activity_service: ActivityService = Depends(get_activity_service),
):
    return await activity_service.get_activity(user, activity_id)