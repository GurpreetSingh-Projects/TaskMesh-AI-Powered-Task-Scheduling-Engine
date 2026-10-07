export type OnboardingQuestionType =
  | "MCQ_SINGLE_SELECT"
  | "MCQ_MULTI_SELECT"
  | "TEXT"
  | "IMAGE"
  | "VIDEO";

export type OnboardingQuestionnaireResponse = {
  items: OnboardingQuestion[];
  total: number;
};

export type OnboardingQuestion = {
  onboarding_question_id: string;
  title: string;
  description: string;
  options: OnboardingQuestionOption[];
  question_type: OnboardingQuestionType;
  is_required: boolean;
  question_order: number;
};

export type OnboardingQuestionOption = {
  title: string;
  description: string;
  option_order: number;
  file_storage_id: string | null;
  image_url: string | null;
};

type QuestionnaireResponse = {
  onboarding_question_id: string;
  question_response: string[];
};
