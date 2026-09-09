export type AuthStackParamList = {
  OnboardingCarousel: undefined;
  Login: undefined;
  Register: undefined;
};

export type UserState = {
  user_id: string;
  email: string;
  profile_img: string | null;
  role: string;
  is_onboarding_completed: boolean;
  is_profile_completed: boolean;
  is_deleted: boolean;
  deleted_at: string | null;
  created_by: string | null;
  updated_by: string | null;
  created_at: string;
  updated_at: string;
};
