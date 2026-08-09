from app.core.enums import ActivationStatus
from app.features.onboarding.enums import OnboardingQuestionType
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, String, Enum as SAEnum, DateTime, Boolean, Integer, JSON
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from datetime import datetime
from sqlalchemy import text
import uuid
from app.database import Base

class OnboardingQuestionnaire(Base):
    __tablename__ = "onboarding_questionnaire"

    onboarding_question_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"), default=uuid.uuid4, nullable=False)
    title: Mapped[str]= mapped_column(String(100), nullable=False)
    description: Mapped[str | None]= mapped_column(String(500), nullable=True)
    image_url: Mapped[str]= mapped_column(String(1000), nullable=True)
    status: Mapped[ActivationStatus] = mapped_column(SAEnum(ActivationStatus, name="onboarding_question_status", native_enum= True), nullable=False, default=ActivationStatus.ENABLED, server_default="ENABLED")
    question_type: Mapped[OnboardingQuestionType] = mapped_column(SAEnum(OnboardingQuestionType, name="onboarding_question_stype", native_enum= True), nullable=False, default=OnboardingQuestionType.MCQ_SINGLE_SELECT, server_default="MCQ_SINGLE_SELECT")
    media_source: Mapped[str | None]= mapped_column(String(500), nullable=True)
    options: Mapped[list] = mapped_column(JSON, nullable=True)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, server_default=text("false"))
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_by: Mapped[uuid.UUID]= mapped_column(ForeignKey("users.user_id"), nullable=True)
    updated_by: Mapped[uuid.UUID]= mapped_column(ForeignKey("users.user_id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now(), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now(), server_default=func.now(), onupdate=func.now(), nullable=False)

class OnboardingQuestionnaireResponse(Base):
    __tablename__ = "onboarding_questionnaire_responses"

    onboarding_questionnaire_response_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"), default=uuid.uuid4, nullable=False)
    onboarding_question_id: Mapped[uuid.UUID]= mapped_column(ForeignKey("onboarding_questionnaire.onboarding_question_id"), nullable=False)
    user_id: Mapped[uuid.UUID]= mapped_column(ForeignKey("users.user_id"), nullable=False)
    title: Mapped[str]= mapped_column(String(100), nullable=False)
    description: Mapped[str | None]= mapped_column(String(500), nullable=True)
    image_url: Mapped[str]= mapped_column(String(1000), nullable=True)
    question_response: Mapped[list]= mapped_column(JSON,nullable=True)
    media_source: Mapped[str]= mapped_column(String(500), nullable=True)
    created_by: Mapped[uuid.UUID]= mapped_column(ForeignKey("users.user_id"), nullable=True)
    updated_by: Mapped[uuid.UUID]= mapped_column(ForeignKey("users.user_id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now(), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now(), server_default=func.now(), onupdate=func.now(), nullable=False)