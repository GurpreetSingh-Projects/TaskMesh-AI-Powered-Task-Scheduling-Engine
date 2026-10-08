from fastapi import APIRouter, Depends
from uuid import UUID
from app.features.onboarding.dependencies import get_onboarding_service
from app.features.onboarding.services import OnboardingService
from app.features.onboarding.schemas import OnboardingQuestionnaireRequestSchema, OnboardingQuestionnaireReadResponseSchema, OnboardingQuestionnaireEditRequestSchema, OnboardingQuestionnaireItemSchema, OnboardingQuestionnaireItemRequestSchema, OnboardingResponsesSchema, OnboardingeResponseItemRequestSchema
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/user-onboarding", tags=["User - Onboarding Questionnaire & Responses"], dependencies=[Depends(get_current_user)])

@router.post("/question", status_code=201, response_model= OnboardingQuestionnaireReadResponseSchema, summary="Add Onboarding Question", description="Submit the onboarding questions")
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
    
@router.patch("/question/deactivate/{question_id}", status_code=204, summary="Delete Onboarding Question", description="Delete an existing onboarding question")
async def deactivate_onboarding_question(question_id: UUID, user= Depends(get_current_user), onboarding_service: OnboardingService = Depends(get_onboarding_service)):
    await onboarding_service.deactivate_onboarding_question(question_id, user)

@router.post("/responses", status_code=201, summary="Add Onboarding Responses for user", description="Submit the onboarding responses")
async def add_onboarding_questions_response(onboarding_questions_response: OnboardingQuestionnaireItemRequestSchema, user=Depends(get_current_user), onboarding_service: OnboardingService = Depends(get_onboarding_service)):
    responses = await onboarding_service.add_onboarding_questions_response(onboarding_questions_response, user)
    return responses

@router.get("/responses", response_model= list[OnboardingResponsesSchema], summary="Get Onboarding Responses for user", description="Retrieve the onboarding responses")
async def get_onboarding_responses(user= Depends(get_current_user), onboarding_service: OnboardingService= Depends(get_onboarding_service)):
    response = await onboarding_service.get_onboarding_responses(user)
    return response

@router.patch("/responses/", summary="Update Onboarding Responses for user", description="Update the onboarding responses")
async def edit_onboarding_responses(edit_questions_response: OnboardingeResponseItemRequestSchema, user= Depends(get_current_user), onboarding_service: OnboardingService= Depends(get_onboarding_service)):
    await onboarding_service.edit_onboarding_responses(edit_questions_response, user)

    return {
        "detail": "Onboarding responses updated successfully."
    }