import { baseApi } from "@/api/baseApi";
import { FileType } from "./types";
import ReactNativeBlobUtil from "react-native-blob-util";

const authApi = baseApi.injectEndpoints({
  endpoints: (builder) => ({
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
        profile_img: FileType | null;
      }) => {
        try {
          const parts = [
            { name: "email", data: fields?.email },
            { name: "password", data: fields?.password },
          ];

          if (fields.profile_img) {
            parts.push({
              name: "profile_img",
              filename: fields?.profile_img.name,
              type: fields?.profile_img.type,
              data: ReactNativeBlobUtil.wrap(fields?.profile_img?.uri),
            });
          }

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

    refreshToken: builder.mutation({
      query: (refreshToken) => ({
        url: `/auth/refresh?refresh_token=${refreshToken}`,
        method: "POST",
      }),
    }),
  }),
  overrideExisting: false,
});

export const {
  useLoginMutation,
  useRegisterMutation,
  useRefreshTokenMutation,
} = authApi;
