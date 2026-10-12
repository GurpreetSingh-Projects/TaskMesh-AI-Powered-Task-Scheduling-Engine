const ONBOARDING_MESSAGES: Record<
  number,
  { title: string; description: string }
> = {
  400: {
    title: "Something went wrong!!",
    description: "Please try again later",
  },
  409: {
    title: "Responses Already Exist",
    description: "Your onboarding questionnaire has already been submitted",
  },
  500: {
    title: "Something went wrong!!",
    description: "Please try again later",
  },
};

export const getOnboardingMessage = (statusCode: number) => {
  if (ONBOARDING_MESSAGES[statusCode]) {
    return ONBOARDING_MESSAGES[statusCode];
  }

  return ONBOARDING_MESSAGES[500];
};
