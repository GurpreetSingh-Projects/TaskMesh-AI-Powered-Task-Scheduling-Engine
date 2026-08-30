import { combineReducers, configureStore } from "@reduxjs/toolkit";
import { baseApi } from "../api/baseApi";
import { createMMKV } from "react-native-mmkv";
import { persistReducer, persistStore } from "redux-persist";
import { useDispatch, useSelector } from "react-redux";
import { userReducer } from "@/features/profile/slice/user";
import { authReducer } from "@/features/auth/slice/auth";
import { settingsReducer } from "@/features/settings/slice/settings";

export const mmkvStorage = createMMKV({
  id: "taskmesh-ai",
});

export const mmkvReduxStorage = {
  setItem: (key: string, value: string) => {
    mmkvStorage.set(key, value);
    return Promise.resolve(true);
  },
  getItem: (key: string) => {
    const value = mmkvStorage.getString(key);
    return Promise.resolve(value ?? null);
  },
  removeItem: (key: string) => {
    mmkvStorage.remove(key);
    return Promise.resolve();
  },
};

const appReducer = combineReducers({
  auth: authReducer,
  userProfile: userReducer,
  settings: settingsReducer,
  [baseApi.reducerPath]: baseApi.reducer,
});

const rootReducer = (
  state: ReturnType<typeof appReducer> | undefined,
  action: { type: string },
) => {
  if (action.type === "RESET_STORE") {
    state = undefined;
  }
  return appReducer(state, action);
};

const persistConfig = {
  key: "taskmesh-ai",
  storage: mmkvReduxStorage,
  version: 1,
  whitelist: ["auth", "userProfile", "settings"],
};

const persistedReducer = persistReducer(persistConfig, rootReducer);

export const store = configureStore({
  reducer: persistedReducer,
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: false,
      immutableCheck: false,
      actionCreatorCheck: false,
    }).concat(baseApi.middleware),
  devTools: __DEV__,
});

export const persistor = persistStore(store);

export const resetReduxStore = async () => {
  try {
    store.dispatch({ type: "RESET_STORE" });
    await persistor.purge();
    // mmkvStorage.clearAll();
    return { success: true };
  } catch (error) {
    console.error("Failed to reset Redux store:", error);
    return { success: false, error };
  }
};

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;

// Typed hooks for use throughout the app
export const useAppDispatch = useDispatch.withTypes<AppDispatch>();
export const useAppSelector = useSelector.withTypes<RootState>();
