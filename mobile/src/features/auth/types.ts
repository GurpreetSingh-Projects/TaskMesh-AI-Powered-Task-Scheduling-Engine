import { UserState } from "../profile/slice/user";

export type AuthStackParamList = {
  OnboardingCarousel: undefined;
  Login: undefined;
  Register: undefined;
};

export type DrawerMode = "default" | "success" | "fail";

export type AuthResponse = {
  access_token: string;
  access_token_expires_at: string;
  refresh_token: string;
  refresh_token_expires_at: string;
  token_type: string;
  user: UserState;
  user_settings: string;
};
