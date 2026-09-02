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
    image_url: str | None = None
    options: list[QuestionnaireOptionSchema]
    question_type: OnboardingQuestionType
    media_source: str | None = None
    status: ActivationStatus

class OnboardingQuestionnaireReadResponseSchema(BaseModel):
    items: list [OnboardingQuestionnaireItemSchema]
    total: int

class OnboardingQuestionnaireEditRequestSchema(BaseModel):
    title: str | None = None
    description: str | None = None
    options: list[QuestionnaireOptionSchema] | None = None
    question_type: OnboardingQuestionType | None = None
    media_source: str | None = None
    status: ActivationStatus | None = None
    image_url: str | None = None

class OnboardingQuestionnaireItemRequestSchema(BaseModel):
    onboarding_question_id: UUID
    question_response: str

class OnboardingResponsesSchema(BaseModel):
    onboarding_questionnaire_response_id: UUID
    onboarding_question_id: UUID
    user_id: UUID
    question_response: str | None = None
    question_type: OnboardingQuestionType
    title: str
    description: str | None = None
    image_url: str | None = None
    media_source: str | None = None
    options: list[QuestionnaireOptionSchema]

class OnboardingeResponseItemRequestSchema(BaseModel):
    onboarding_questionnaire_response_id: UUID
    question_response: str