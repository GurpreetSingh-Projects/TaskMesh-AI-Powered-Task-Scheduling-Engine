from fastapi import HTTPException
from uuid import UUID
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import EmailStr
from datetime import datetime, timezone
from app.features.onboarding.models import OnboardingQuestionnaire
from app.features.onboarding.schemas import OnboardingQuestionnaireRequest
    
class OnboardingService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def add_onboarding_questions(self, onboarding_questions: list[OnboardingQuestionnaireRequest]):
        if not onboarding_questions:
            raise HTTPException(status_code=400, detail="No onboarding questions provided.")

        added_questions = []
        try:
            for question in onboarding_questions:
                if not question.title or not question.options or not question.question_type:
                    raise HTTPException(status_code=400, detail="Each question must have a title, options, and question type.")

                query = insert(OnboardingQuestionnaire).values(
                    title=question.title,
                    description=question.description,
                    options=question.options,
                    question_type=question.question_type,
                    media_source=question.media_source
                )
                added_question = await self.db.execute(query)
                added_questions.append(added_question)

        except Exception as e:
            await self.db.rollback()
            raise HTTPException(status_code=500, detail=f"An error occurred while adding onboarding questions: {str(e)}")

        await self.db.commit()

        return onboarding_questions