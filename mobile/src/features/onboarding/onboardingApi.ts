import { baseApi } from "@/api/baseApi";
import {
  OnboardingQuestionnaireResponse,
  OnboardingQuestionsAnswersRequest,
} from "./types";

const onboardingApi = baseApi.injectEndpoints({
  endpoints: (builder) => ({
    onboardingQuestionnaire: builder.query<
      OnboardingQuestionnaireResponse,
      void
    >({
      query: () => "/user-onboarding/questions",
    }),

    createOnboardingQuestionnaireResponses: builder.mutation<
      OnboardingQuestionnaireResponse,
      OnboardingQuestionsAnswersRequest
    >({
      query: (body) => ({
        url: "/user-onboarding/responses",
        method: "POST",
        body,
      }),
    }),
  }),
  overrideExisting: false,
});

export const {
  useLazyOnboardingQuestionnaireQuery,
  useCreateOnboardingQuestionnaireResponsesMutation,
} = onboardingApi;
