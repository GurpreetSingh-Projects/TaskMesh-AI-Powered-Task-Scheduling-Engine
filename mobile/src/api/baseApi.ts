import { getAccessToken } from "@/features/auth/utils";
import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";
import ReactNativeBlobUtil from "react-native-blob-util";
import {
  OnboardingQuestionnaireResponse,
  OnboardingQuestionsAnswersRequest,
} from "@/features/onboarding/types";
import * as SecureStore from "expo-secure-store";
import { FileType } from "@/features/auth/types";

export const ACCESS_TOKEN_KEY = "accessToken";

export const baseApi = createApi({
  reducerPath: "baseApi",
  baseQuery: fetchBaseQuery({
    baseUrl: `${process.env.EXPO_PUBLIC_API_URL}`,
    prepareHeaders: async (headers) => {
      try {
        const token = await SecureStore.getItemAsync(ACCESS_TOKEN_KEY);
        if (token) headers.set("Authorization", `Bearer ${token}`);
        return headers;
      } catch (error) {
        console.log(error);
      }
    },
  }),

  endpoints: (builder) => ({
    awakeServer: builder.query<void, void>({
      query: () => "/awake",
    }),
  }),
});

export const { useLazyAwakeServerQuery } = baseApi;
