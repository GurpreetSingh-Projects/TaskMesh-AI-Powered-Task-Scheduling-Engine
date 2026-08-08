from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from uuid import UUID
from pydantic import EmailStr
from app.features.onboarding.dependencies import get_onboarding_service
from app.features.onboarding.services import OnboardingService
from app.features.onboarding.schemas import OnboardingQuestionnaireRequest, OnboardingQuestionnaireResponse
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/user-onboarding", tags=["User - Onboarding Questionnaire & Responses"], dependencies=[Depends(get_current_user)])

@router.post("/question", 

            #  response_model= list[OnboardingQuestionnaireResponse], 
             summary="Add Onboarding Question", description="Submit the onboarding questions")
async def add_onboarding_questions(onboarding_questions: list[OnboardingQuestionnaireRequest], user=Depends(get_current_user), get_onboarding_service: OnboardingService = Depends(get_onboarding_service)):
    questions = await get_onboarding_service.add_onboarding_questions(user, onboarding_questions)
    return questions

@router.get("/questions", response_model= list[OnboardingQuestionnaireResponse], summary="Get Onboarding Questions", description="Retrieve all onboarding questions")
async def get_onboarding_questions(user=Depends(get_current_user), get_onboarding_service: OnboardingService = Depends(get_onboarding_service)):
    questions= await get_onboarding_service.get_onboarding_questions(user)
    return questions

@router.patch("/question/{question_id}", response_model= OnboardingQuestionnaireResponse, summary="Update Onboarding Question", description="Update an existing onboarding question")
async def update_onboarding_question(question_id: UUID):
    pass

@router.patch("/question/deactivate/{question_id}", summary="Delete Onboarding Question", description="Delete an existing onboarding question")
async def deactivate_onboarding_question(question_id: UUID):
    pass

@router.post("/responses", summary="Add Onboarding Responses for user", description="Submit the onboarding responses")
async def add_onboarding_response():
    pass

@router.get("/responses", summary="Get Onboarding Responses for user", description="Retrieve the onboarding responses")
async def get_onboarding_responses():
    pass

@router.patch("/responses/", summary="Update Onboarding Responses for user", description="Update the onboarding responses")
async def update_onboarding_responses():
    pass 