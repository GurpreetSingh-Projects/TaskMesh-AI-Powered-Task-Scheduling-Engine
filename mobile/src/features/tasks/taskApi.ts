import { ACCESS_TOKEN_KEY, baseApi } from "@/api/baseApi";
import ReactNativeBlobUtil from "react-native-blob-util";
import * as SecureStore from "expo-secure-store";
import { FileType } from "../auth/types";
import { TASK_PRIORITY, TASK_STATUS } from "./utils";
import { TasksGetResponse } from "./types";

const taskApi = baseApi.injectEndpoints({
  endpoints: (builder) => ({
    getTasks: builder.query<TasksGetResponse, void>({
      query: () => "/tasks",
    }),
    createTask: builder.mutation({
      queryFn: async (fields: {
        title: string;
        description?: string;
        due_at?: string | null;
        status: (typeof TASK_STATUS)[number];
        priority: (typeof TASK_PRIORITY)[number];
        task_img: FileType;
      }) => {
        try {
          const parts = [];

          if (fields?.title)
            parts.push({
              name: "title",
              data: fields.title,
            });

          if (fields?.description)
            parts.push({
              name: "description",
              data: fields.description,
            });

          if (fields?.due_at)
            parts.push({
              name: "due_at",
              data: fields.due_at,
            });

          if (fields?.status)
            parts.push({
              name: "status",
              data: fields.status,
            });

          if (fields?.priority)
            parts.push({
              name: "priority",
              data: fields.priority,
            });

          if (fields?.task_img && fields?.task_img?.uri) {
            parts.push({
              name: "task_img",
              filename: fields?.task_img.name,
              type: fields?.task_img.type,
              data: ReactNativeBlobUtil.wrap(fields?.task_img?.uri),
            });
          }

          const token = await SecureStore.getItemAsync(ACCESS_TOKEN_KEY);
          const response = await ReactNativeBlobUtil.fetch(
            "POST",
            `${process.env.EXPO_PUBLIC_API_URL}/tasks`,
            {
              Authorization: `Bearer ${token}`,
              "Content-Type": "multipart/form-data",
            },
            parts,
          );

          const status_code = response.info().status;
          const data = response.json();

          return status_code == 200 || status_code == 201
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
    updateTask: builder.mutation({
      queryFn: {},
    }),
  }),
  overrideExisting: true,
});

export const { useCreateTaskMutation, useGetTasksQuery } = taskApi;
