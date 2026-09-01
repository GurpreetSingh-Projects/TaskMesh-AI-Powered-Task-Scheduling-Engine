from fastapi import HTTPException
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, func
from datetime import datetime, timezone
from uuid import UUID
from app.features.onboarding.models import OnboardingQuestionnaire
from app.features.onboarding.schemas import OnboardingQuestionnaireRequestSchema, OnboardingQuestionnaireEditRequestSchema
from app.features.users.models import Users
    
class OnboardingService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def add_onboarding_questions(self, user: Users, onboarding_questions: list[OnboardingQuestionnaireRequestSchema]):
        if not onboarding_questions:
            raise HTTPException(status_code= 400, detail="No onboarding questions provided.")

        values_list = []
        try:
            now = datetime.now(timezone.utc)

            for question in onboarding_questions:
                if not question.title or not question.options or not question.question_type:
                    raise HTTPException(status_code=400, detail="Each question must have a title, options, and question type.")

                values_list.append({
                    "title": question.title,
                    "description": question.description,
                    "question_type": question.question_type,
                    "options":  [option.model_dump(mode= "json") for option in question.options],
                    "media_source": question.media_source,
                    "updated_by":  user.user_id,
                    "updated_at":  now,
                    "created_by":  user.user_id,
                    "created_at":  now,   
                })                       
                      
            query = insert(OnboardingQuestionnaire).values(
                values_list
            ).returning(OnboardingQuestionnaire)

            added_questions = (await self.db.execute(query)).scalars().all()
            
        except HTTPException:
            await self.db.rollback()
            raise

        except Exception as e:
            await self.db.rollback()
            raise HTTPException(status_code=500, detail=f"An error occurred while adding onboarding questions: {str(e)}")

        await self.db.commit()

        count_query = select(func.count(OnboardingQuestionnaire.onboarding_question_id)).where(OnboardingQuestionnaire.status == "ENABLED", OnboardingQuestionnaire.is_deleted.is_(False))
        
        total = (await self.db.execute(count_query)).scalar_one()
        
        return {
                "items": added_questions,
                "total": total
        }

    async def get_onboarding_questions(self):
        query= select(OnboardingQuestionnaire).where(OnboardingQuestionnaire.status == "ENABLED", OnboardingQuestionnaire.is_deleted.is_(False)).limit(25)

        questions = (await self.db.execute(query)).scalars().all()

        count_query = select(func.count(OnboardingQuestionnaire.onboarding_question_id)).where(OnboardingQuestionnaire.status == "ENABLED", OnboardingQuestionnaire.is_deleted.is_(False))

        total = (await self.db.execute(count_query)).scalar_one()

        return {
            "items": questions,
            "total": total
        }

    async def edit_onboarding_question(self, question_id: UUID, question_data: OnboardingQuestionnaireEditRequestSchema, user: Users):
        updated_question= question_data.model_dump(exclude_unset= True, mode="json")

        if not updated_question:
            raise HTTPException(status_code= 400, detail= "Invalid question data provided")
        
        updated_question["updated_by"]= user.user_id

        query= (
            update(OnboardingQuestionnaire)
                .where(OnboardingQuestionnaire.onboarding_question_id == question_id)
                .values(**updated_question)
                .returning(OnboardingQuestionnaire)
        )

        try:
            result= (await self.db.execute(query)).scalar_one_or_none()
            if not result:
                raise HTTPException(status_code= 404, detail= "No onboarding question found for the entered question_id")
            await self.db.commit()
            return result
        
        except HTTPException:
            await self.db.rollback()
            raise

        except Exception as e:
            await self.db.rollback()
            raise HTTPException(status_code=500, detail=f"An error occurred while updating onboarding question: {str(e)}")

    async def deactivate_onboarding_question(self, question_id: UUID, user: Users):
        updated_question={
            "updated_by": user.user_id,
            "is_deleted": True,
            "deleted_at": datetime.now(timezone.utc)
        }

        query= (
            update(OnboardingQuestionnaire)
                .where(OnboardingQuestionnaire.onboarding_question_id == question_id)
                .values(**updated_question)
                .returning(OnboardingQuestionnaire)
        )

        result = (await self.db.execute(query)).scalar_one_or_none()

        if not result:
            raise HTTPException(status_code= 404, detail= "No onboarding question found for the entered question_id")
        await self.db.commit()
        return