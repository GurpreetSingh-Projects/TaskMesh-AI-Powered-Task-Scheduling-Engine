from pydantic import BaseModel

class QuestionnaireOption(BaseModel):
    title: str
    description: str | None = None
    image_url: str | None = None

class OnboardingQuestionnaireRequest(BaseModel):
    title: str
    description: str | None = None
    options: list[QuestionnaireOption]
    question_type: str
    media_source: str | None = None

# class OnboardingQuestionnaireResponse(BaseModel):