from enum import Enum

class OnboardingQuestionType(str, Enum):
    MCQ_SINGLE_SELECT = "MCQ_SINGLE_SELECT"
    MCQ_MULTI_SELECT = "MCQ_MULTI_SELECT"
    TEXT = "TEXT"
    IMAGE = "IMAGE"
    VIDEO = "VIDEO"