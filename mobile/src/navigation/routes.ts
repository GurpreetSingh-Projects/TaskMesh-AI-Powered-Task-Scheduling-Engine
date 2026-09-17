import type { NativeStackNavigationProp } from "@react-navigation/native-stack";

export type RootStackParamList = {
  Auth: undefined;
  Dashboard: undefined;
};

export type AuthStackParamList = {
  OnboardingCarousel: undefined;
  Login: undefined;
  Register: undefined;
};

export type HomeStackParamList = {
  OnboardingQuestionnaire: undefined;
  ProfileDetailsPending: undefined;
  Home: undefined;
};

export type RootStackNavigationProp =
  NativeStackNavigationProp<RootStackParamList>;

export type AuthStackNavigationProp =
  NativeStackNavigationProp<AuthStackParamList>;

export type HomeStackNavigationProp =
  NativeStackNavigationProp<HomeStackParamList>;
