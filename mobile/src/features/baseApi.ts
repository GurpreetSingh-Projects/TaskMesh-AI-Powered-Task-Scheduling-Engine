import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";

export const baseApi = createApi({
  reducerPath: "baseApi",
  baseQuery: fetchBaseQuery({ baseUrl: `${process.env.EXPO_PUBLIC_API_URL}` }),
  endpoints: (builder) => ({
    awakeServer: builder.query<ResponseType, void>({
      query: () => "/",
    }),

    signIn: builder.mutation({
      query: ({ email, password }) => ({
        url: "/auth/login",
        method: "POST",
        body: {
          useranme: email,
          password,
        },
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
      }),
    }),

    // register: builder.mutation({
    //   query: ({ email, password }) => ({
    //     url: "/auth/register",
    //     method: "POST",
    //     body: {
    //       useranme: email,
    //       password,
    //     },
    //   }),
    // }),
    register: builder.mutation({
      query: ({ email, password }) => ({
        url: "/users/create",
        method: "POST",
        body: {
          email: email,
          password,
        },
      }),
    }),
  }),
});

export const { useLazyAwakeServerQuery, useSignInMutation } = baseApi;
