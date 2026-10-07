from pydantic import BaseModel, RootModel
from uuid import UUID
from app.core.enums import ActivationStatus
from app.features.onboarding.enums import OnboardingQuestionType

class QuestionnaireOptionSchema(BaseModel):
    title: str
    description: str | None = None
    option_order: int
    file_storage_id: UUID | None = None

class QuestionnaireOptionReadSchema(QuestionnaireOptionSchema):
    image_url: str | None

class OnboardingQuestionnaireRequestSchema(BaseModel):
    title: str
    description: str | None = None
    options: list[QuestionnaireOptionSchema]
    question_type: OnboardingQuestionType
    is_required: bool
    question_order: int = 0

class OnboardingQuestionnaireItemSchema(BaseModel):
    onboarding_question_id: UUID
    title: str
    description: str | None = None
    options: list[QuestionnaireOptionReadSchema]
    question_type: OnboardingQuestionType
    is_required: bool
    question_order: int

class OnboardingQuestionnaireReadResponseSchema(BaseModel):
    items: list[OnboardingQuestionnaireItemSchema]
    total: int

class OnboardingQuestionnaireEditRequestSchema(BaseModel):
    title: str | None = None
    description: str | None = None
    options: list[QuestionnaireOptionSchema] | None = None
    question_type: OnboardingQuestionType | None = None
    status: ActivationStatus | None = None
    is_required: bool | None = None
    question_order: int | None = None

class OnboardingQuestionnaireItemRequestSchema(RootModel[dict[UUID, list]]):
    pass

class OnboardingResponsesSchema(BaseModel):
    onboarding_questionnaire_response_id: UUID
    onboarding_question_id: UUID
    user_id: UUID
    file_storage_id: UUID | None = None
    question_response: list | None = None
    question_type: OnboardingQuestionType
    title: str
    description: str | None = None
    is_required: bool
    question_order: int
    options: list[QuestionnaireOptionReadSchema]

class OnboardingeResponseItemRequestSchema(BaseModel):
    onboarding_questionnaire_response_id: UUID
    question_response: list