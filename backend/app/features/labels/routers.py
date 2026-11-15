from uuid import UUID

from fastapi import APIRouter, Depends, File, Form, UploadFile

from app.core.dependencies import require_roles
from app.features.labels.dependencies import get_labels_service
from app.features.labels.schemas import (
    GetLabelsSchema,
    LabelCreateSchema,
    LabelResponseSchema,
)
from app.features.labels.services import LabelsService
from app.features.users.enums import UserRoles

router = APIRouter(prefix="/labels", tags=["Labels"])


@router.post("", response_model=LabelResponseSchema, summary="Create a new label")
async def create_label(
    title: str = Form(...),
    description: str | None = Form(None),
    entity_type: str | None = Form(None),
    entity_id: UUID | None = Form(None),
    label_img: UploadFile | None = File(None),
    user=Depends(require_roles([UserRoles.ADMIN, UserRoles.USER])),
    label_service: LabelsService = Depends(get_labels_service),
):
    label_data = LabelCreateSchema(
        title=title,
        description=description,
        entity_type=entity_type,
        entity_id=entity_id,
    )

    response = await label_service.create_label(
        user=user,
        label_data=label_data,
        label_img=label_img,
    )

    return response


@router.get("", response_model=GetLabelsSchema, summary="Get all labels")
async def get_labels(
    limit: int = 20,
    user=Depends(require_roles([UserRoles.ADMIN, UserRoles.USER])),
    label_service: LabelsService = Depends(get_labels_service),
):
    response = await label_service.get_labels(
        user=user,
        limit=limit,
    )

    return response


@router.patch(
    "/{label_id}",
    response_model=LabelResponseSchema,
    summary="Update or deactivate a label",
)
async def update_label(
    label_id,
    label_data,
    user=Depends(require_roles([UserRoles.ADMIN])),
    label_service: LabelsService = Depends(get_labels_service),
):
    response = await label_service.update_label(
        user_id=user.user_id,
        label_id=label_id,
        label_data=label_data,
    )

    return response


@router.get("/{label_id}", response_model=LabelResponseSchema, summary="Get a label")
async def get_label(
    label_id,
    user=Depends(require_roles([UserRoles.ADMIN, UserRoles.USER])),
    label_service: LabelsService = Depends(get_labels_service),
):
    response = await label_service.get_label(
        user_id=user.user_id,
        label_id=label_id,
    )

    return response
