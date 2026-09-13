import { configureStore } from "@reduxjs/toolkit";
import { userSlice } from "../features/auth/user";
import { baseApi } from "../api/baseApi";
export const store = configureStore({
  reducer: {
    user: userSlice.reducer,
    [baseApi.reducerPath]: baseApi.reducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: false,
      immutableCheck: false,
      actionCreatorCheck: false,
    }).concat(baseApi.middleware),
  devTools: false,
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
