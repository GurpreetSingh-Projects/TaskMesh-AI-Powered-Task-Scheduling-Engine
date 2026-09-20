import * as SecureStore from "expo-secure-store";
import { AuthResponse } from "./types";
import { store } from "@/app/store";
import { setUserInfo } from "../profile/slice/user";
import { setAuthInfo } from "./slice/auth";

const ACCESS_TOKEN_KEY = "accessToken";
const REFRESH_TOKEN_KEY = "refreshToken";

export const setAccessToken = async (value: string) => {
  await SecureStore.setItemAsync(ACCESS_TOKEN_KEY, value);
};

export const setRefreshToken = async (value: string) => {
  await SecureStore.setItemAsync(REFRESH_TOKEN_KEY, value);
};

export const getAccessToken = async (): Promise<string | null> => {
  return await SecureStore.getItemAsync(ACCESS_TOKEN_KEY);
};

export const getRefreshToken = async (): Promise<string | null> => {
  return await SecureStore.getItemAsync(REFRESH_TOKEN_KEY);
};

export const deleteAccessToken = async () => {
  await SecureStore.deleteItemAsync(ACCESS_TOKEN_KEY);
};

export const deleteRefreshToken = async () => {
  await SecureStore.deleteItemAsync(REFRESH_TOKEN_KEY);
};

export const clearTokens = async () => {
  await Promise.all([deleteAccessToken(), deleteRefreshToken()]);
};

export const setAuth = async (authResponse: AuthResponse) => {
  let hasAccessToken = false,
    hasRefreshToken = false;

  if (authResponse?.access_token) {
    await setAccessToken(authResponse.access_token);
    hasAccessToken = true;
  }

  if (authResponse?.refresh_token) {
    await setRefreshToken(authResponse.refresh_token);
    hasRefreshToken = true;
  }

  store.dispatch(setUserInfo(authResponse?.user));
  store.dispatch(
    setAuthInfo({
      token_type: authResponse.token_type,
      hasAccessToken,
      hasRefreshToken,
      last_login_at: new Date().toISOString(),
      last_refresh_at: null,
      isAuthenticated: hasAccessToken && hasRefreshToken,
      accessTokenExpiresAt: new Date(authResponse.access_token_expires_at),
      refreshTokenExpiresAt: new Date(authResponse.refresh_token_expires_at),
    }),
  );
};

const AUTH_MESSAGES: Record<number, { title: string; description: string }> = {
  404: { title: "Oops!!", description: "Invalid email id or password" },
  409: {
    title: "Already Registered",
    description: "This email address is already in use",
  },
  500: {
    title: "Something went wrong!!",
    description: "Please try again later",
  },
};

export const getAuthMessage = (statusCode: number) => {
  if (AUTH_MESSAGES[statusCode]) {
    return AUTH_MESSAGES[statusCode];
  }
  return {
    title: "Oops!!",
    description: "Something went wrong. Please try again later",
  };
};
