from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from uuid import UUID
from pydantic import EmailStr
from app.features.onboarding.dependencies import get_onboarding_service
from app.features.onboarding.services import OnboardingService
from app.features.onboarding.schemas import OnboardingQuestionnaireRequestSchema, OnboardingQuestionnaireReadResponseSchema, OnboardingQuestionnaireEditRequestSchema, OnboardingQuestionnaireItemSchema
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/user-onboarding", tags=["User - Onboarding Questionnaire & Responses"], dependencies=[Depends(get_current_user)])

@router.post("/question", response_model= OnboardingQuestionnaireReadResponseSchema, summary="Add Onboarding Question", description="Submit the onboarding questions")
async def add_onboarding_questions(onboarding_questions: list[OnboardingQuestionnaireRequestSchema], user=Depends(get_current_user), get_onboarding_service: OnboardingService = Depends(get_onboarding_service)):
    questions = await get_onboarding_service.add_onboarding_questions(user, onboarding_questions)
    return questions

@router.get("/questions", response_model= OnboardingQuestionnaireReadResponseSchema, summary="Get Onboarding Questions", description="Retrieve all onboarding questions")
async def get_onboarding_questions(user= Depends(get_current_user), onboarding_service: OnboardingService = Depends(get_onboarding_service)):
    questions= await onboarding_service.get_onboarding_questions()
    return questions

@router.patch("/question/{question_id}", response_model= OnboardingQuestionnaireItemSchema, summary="Updates Onboarding Question", description="Update an existing onboarding question")
async def update_onboarding_question(question_id: UUID, question_data: OnboardingQuestionnaireEditRequestSchema, user= Depends(get_current_user), onboarding_service: OnboardingService = Depends(get_onboarding_service)):
    updated_question= await onboarding_service.edit_onboarding_question(question_id, question_data, user)
    return updated_question
    
@router.patch("/question/deactivate/{question_id}", summary="Delete Onboarding Question", description="Delete an existing onboarding question")
async def deactivate_onboarding_question(question_id: UUID, user= Depends(get_current_user), onboarding_service: OnboardingService = Depends(get_onboarding_service)):
    deactivated_onboarding_question= await onboarding_service.deactivate_onboarding_question(question_id, user)
    return {"detail": "Onboarding question deactivated successfully"}

@router.post("/responses", summary="Add Onboarding Responses for user", description="Submit the onboarding responses")
async def add_onboarding_response():
    pass

@router.get("/responses", summary="Get Onboarding Responses for user", description="Retrieve the onboarding responses")
async def get_onboarding_responses():
    pass

@router.patch("/responses/", summary="Update Onboarding Responses for user", description="Update the onboarding responses")
async def update_onboarding_responses():
    pass 