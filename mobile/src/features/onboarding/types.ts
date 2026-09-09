export type OnboardingQuestionType =
  | "MCQ_SINGLE_SELECT"
  | "MCQ_MULTI_SELECT"
  | "TEXT"
  | "IMAGE"
  | "VIDEO";

export type QuestionnaireOption = {
  title: string;
  description: string;
  image_url: string;
};

export type OnboardingQuestionnaireItem = {
  onboarding_question_id: string;
  title: string;
  description: string;
  image_url: string | null;
  options: QuestionnaireOption[];
  question_type: OnboardingQuestionType;
  media_source: string;
};

export type OnboardingQuestionnaireResponse = {
  items: OnboardingQuestionnaireItem[];
  total: number;
};
