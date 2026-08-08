from pydantic import BaseModel
from uuid import UUID
from app.core.enums import ActivationStatus
from app.features.onboarding.enums import OnboardingQuestionType

class QuestionnaireOption(BaseModel):
    title: str
    description: str | None = None
    image_url: str | None = None

class OnboardingQuestionnaireRequest(BaseModel):
    title: str
    description: str | None = None
    options: list[QuestionnaireOption]
    question_type: OnboardingQuestionType
    media_source: str | None = None

class OnboardingQuestionnaireResponse(BaseModel):
    onboarding_question_id: UUID
    title: str
    description: str | None = None
    options: list[QuestionnaireOption]
    question_type: OnboardingQuestionType
    media_source: str | None = None
    status: ActivationStatus
    image_url: str | None = None