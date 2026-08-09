from pydantic import BaseModel
from uuid import UUID
from app.core.enums import ActivationStatus
from app.features.onboarding.enums import OnboardingQuestionType

class QuestionnaireOptionSchema(BaseModel):
    title: str
    description: str | None = None
    image_url: str | None = None

class OnboardingQuestionnaireRequestSchema(BaseModel):
    title: str
    description: str | None = None
    options: list[QuestionnaireOptionSchema]
    question_type: OnboardingQuestionType
    media_source: str | None = None

class OnboardingQuestionnaireItemSchema(BaseModel):
    onboarding_question_id: UUID
    title: str
    description: str | None = None
    options: list[QuestionnaireOptionSchema]
    question_type: OnboardingQuestionType
    media_source: str | None = None
    status: ActivationStatus
    image_url: str | None = None

class OnboardingQuestionnaireReadResponseSchema(BaseModel):
    items: list [OnboardingQuestionnaireItemSchema]
    total: int

class OnboardingQuestionnaireEditRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    options: list[QuestionnaireOptionSchema]
    question_type: OnboardingQuestionType
    media_source: str | None = None
    status: ActivationStatus
    image_url: str | None = None