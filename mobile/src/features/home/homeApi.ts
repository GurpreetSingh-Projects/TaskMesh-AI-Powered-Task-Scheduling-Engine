import { ACCESS_TOKEN_KEY, baseApi } from "@/api/baseApi";

const homeApi = baseApi.injectEndpoints({
  endpoints: (builder) => ({
    getSummary: builder.query({
      query: ({ start_date, end_date, limit }) => ({
        url: "/tasks/summary",
        params: { start_date, end_date, limit },
      }),
    }),
  }),
  overrideExisting: true,
});

export const { useGetSummaryQuery } = homeApi;
