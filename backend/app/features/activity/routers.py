from uuid import UUID

from fastapi import APIRouter, Depends, File, Form, Query, UploadFile

from app.core.dependencies import require_roles
from app.features.activity.dependencies import get_activity_service
from app.features.activity.enums import UserActivityType
from app.features.activity.schemas import (
    UserActivityCreateRequestSchema,
    UserActivityReadResponseSchema,
)
from app.features.activity.services import ActivityService
from app.features.users.enums import UserRoles

router = APIRouter(prefix="/activity", tags=["Activity"])


@router.post("", response_model=UserActivityReadResponseSchema)
async def create_activity(
    activity_type: UserActivityType,
    user_device_id: str | None = None,
    entity_type: str | None = None,
    entity_id: UUID | None = None,
    user=Depends(require_roles([UserRoles.ADMIN])),
    activity_service: ActivityService = Depends(get_activity_service),
):
    activity_data = UserActivityCreateRequestSchema(
        activity_type=activity_type,
        user_device_id=user_device_id,
        entity_type=entity_type,
        entity_id=entity_id,
    )
    return await activity_service.create_activity(user, activity_data)


@router.get("", response_model=list[UserActivityReadResponseSchema])
async def get_activities(
    user=Depends(require_roles([UserRoles.ADMIN])),
    limit: int = Query(default=10, gt=0, le=100),
    activity_service: ActivityService = Depends(get_activity_service),
):
    return await activity_service.get_activities(limit, user)


@router.get("/{activity_id}", response_model=UserActivityReadResponseSchema)
async def get_activity(
    activity_id: UUID,
    user=Depends(require_roles([UserRoles.ADMIN])),
    activity_service: ActivityService = Depends(get_activity_service),
):
    return await activity_service.get_activity(user, activity_id)
