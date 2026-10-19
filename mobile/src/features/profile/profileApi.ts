import { ACCESS_TOKEN_KEY, baseApi } from "@/api/baseApi";
import ReactNativeBlobUtil from "react-native-blob-util";
import * as SecureStore from "expo-secure-store";
import { FileType } from "../auth/types";

const profileApi = baseApi.injectEndpoints({
  endpoints: (builder) => ({
    updateProfile: builder.mutation({
      queryFn: async (fields: {
        fullName: string | null;
        profile_img: FileType;
      }) => {
        try {
          const parts = [];

          if (fields?.fullName)
            parts.push({ name: "full_name", data: fields?.fullName });
          else parts.push({ name: "full_name", data: null });

          if (fields?.profile_img && fields?.profile_img?.uri) {
            parts.push({
              name: "profile_img",
              filename: fields?.profile_img.name,
              type: fields?.profile_img.type,
              data: ReactNativeBlobUtil.wrap(fields?.profile_img?.uri),
            });
          } else parts.push({ name: "profile_img", data: null });

          const token = await SecureStore.getItemAsync(ACCESS_TOKEN_KEY);
          const response = await ReactNativeBlobUtil.fetch(
            "PATCH",
            `${process.env.EXPO_PUBLIC_API_URL}/users/edit`,
            {
              Authorization: `Bearer ${token}`,
              "Content-Type": "multipart/form-data",
            },
            parts,
          );

          const status_code = response.info().status;
          const data = response.json();

          return status_code == 200
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
  }),
  overrideExisting: true,
});

export const { useUpdateProfileMutation } = profileApi;
