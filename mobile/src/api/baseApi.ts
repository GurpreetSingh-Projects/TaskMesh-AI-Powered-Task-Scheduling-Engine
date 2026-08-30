import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";

export const baseApi = createApi({
  reducerPath: "baseApi",
  baseQuery: fetchBaseQuery({ baseUrl: `${process.env.EXPO_PUBLIC_API_URL}` }),
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
      query: ({ email, password }) => ({
        url: "/auth/register",
        method: "POST",
        body: {
          email,
          password,
        },
      }),
    }),
  }),
});

export const {
  useLazyAwakeServerQuery,
  useLoginMutation,
  useRegisterMutation,
} = baseApi;
