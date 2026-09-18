import { createSlice, PayloadAction } from "@reduxjs/toolkit";

export type AuthState = {
  token_type: string;
  hasAccessToken: boolean;
  hasRefreshToken: boolean;
  last_login_at: string | null;
  last_refresh_at: string | null;
  isAuthenticated: boolean;
  accessTokenExpiresAt: Date | null;
  refreshTokenExpiresAt: Date | null;
};

const initialState: AuthState = {
  token_type: "",
  hasAccessToken: false,
  hasRefreshToken: false,
  last_login_at: null,
  last_refresh_at: null,
  isAuthenticated: false,
  accessTokenExpiresAt: null,
  refreshTokenExpiresAt: null,
};

export const authSlice = createSlice({
  name: "auth",
  initialState,
  reducers: {
    setAuthInfo: (state, action: PayloadAction<AuthState>) => {
      state.token_type = action.payload.token_type;
      state.hasAccessToken = action.payload.hasAccessToken;
      state.hasRefreshToken = action.payload.hasRefreshToken;
      state.last_login_at = action.payload.last_login_at;
      state.last_refresh_at = action.payload.last_refresh_at;
      state.isAuthenticated = action.payload.isAuthenticated;
      state.accessTokenExpiresAt = action.payload.accessTokenExpiresAt;
      state.refreshTokenExpiresAt = action.payload.refreshTokenExpiresAt;
    },
    setTokenType: (state, action: PayloadAction<string>) => {
      state.token_type = action.payload;
    },
    setHasAccessToken: (state, action: PayloadAction<boolean>) => {
      state.hasAccessToken = action.payload;
    },
    setHasRefreshToken: (state, action: PayloadAction<boolean>) => {
      state.hasRefreshToken = action.payload;
    },
    setLastLoginAt: (state, action: PayloadAction<string | null>) => {
      state.last_login_at = action.payload;
    },
    setLastRefreshAt: (state, action: PayloadAction<string | null>) => {
      state.last_refresh_at = action.payload;
    },
    setIsAuthenticated: (state, action: PayloadAction<boolean>) => {
      state.isAuthenticated = action.payload;
    },
    setAccessTokenExpiresAt: (state, action: PayloadAction<string | null>) => {
      state.accessTokenExpiresAt = new Date(action.payload);
    },
    setRefreshTokenExpiresAt: (state, action: PayloadAction<string | null>) => {
      state.refreshTokenExpiresAt = new Date(action.payload);
    },
    clearAuth: () => ({
      ...initialState,
    }),
  },
});

export const {
  setAuthInfo,
  setTokenType,
  setHasAccessToken,
  setHasRefreshToken,
  setLastLoginAt,
  setLastRefreshAt,
  setIsAuthenticated,
  setAccessTokenExpiresAt,
  setRefreshTokenExpiresAt,
  clearAuth,
} = authSlice.actions;

export const authReducer = authSlice.reducer;
