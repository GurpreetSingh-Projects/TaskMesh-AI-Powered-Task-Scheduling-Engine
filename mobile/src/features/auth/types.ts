import { UserState } from "../profile/types";

export type DrawerMode = "default" | "success" | "fail" | "mediaSelection";

export type AuthResponse = {
  access_token: string;
  access_token_expires_at: string;
  refresh_token: string;
  refresh_token_expires_at: string;
  token_type: string;
  user: UserState;
  user_settings: string;
};

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

export type FileType = {
  name: string;
  type: string;
  uri: string | null;
};
