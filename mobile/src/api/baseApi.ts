import { getAccessToken } from "@/features/auth/utils";
import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";
import ReactNativeBlobUtil from "react-native-blob-util";
import * as SecureStore from "expo-secure-store";
import { OnboardingQuestionnaireResponse } from "@/features/onboarding/types";

const ACCESS_TOKEN_KEY = "accessToken";

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
    awakeServer: builder.query<ResponseType, void>({
      query: () => "/awake",
    }),

    login: builder.mutation({
      query: ({ email, password }) => ({
        url: "/auth/login",
        method: "POST",
        body: {
          email,
          password,
        },
      }),
    }),

    register: builder.mutation({
      queryFn: async (fields: {
        email: string;
        password: string;
        profile_img: string | null;
      }) => {
        try {
          const parts = [
            { name: "email", data: fields?.email },
            { name: "password", data: fields?.password },
            {
              name: "profile_img",
              filename: fields?.profile_img.name,
              type: fields?.profile_img.type,
              data: fields?.profile_img?.uri
                ? ReactNativeBlobUtil.wrap(fields?.profile_img?.uri)
                : null,
            },
          ];

          const response = await ReactNativeBlobUtil.fetch(
            "POST",
            `${process.env.EXPO_PUBLIC_API_URL}/auth/register`,
            { "Content-Type": "multipart/form-data" },
            parts,
          );

          const status_code = response.info().status;
          const data = response.json();

          return status_code == 201
            ? { data }
            : {
                error: {
                  status_code,
                  data,
                },
              };
        } catch (error) {
          return { error: { status: "FETCH_ERROR", error: String(error) } };
        }
      },
    }),

    onboardingQuestionnaire: builder.query<
      OnboardingQuestionnaireResponse,
      void
    >({
      query: () => "/user-onboarding/questions",
    }),
  }),
});

export const {
  useLazyAwakeServerQuery,
  useLoginMutation,
  useRegisterMutation,
  useLazyOnboardingQuestionnaireQuery,
} = baseApi;
