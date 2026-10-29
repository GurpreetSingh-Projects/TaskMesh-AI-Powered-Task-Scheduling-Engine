import type { NativeStackNavigationProp } from "@react-navigation/native-stack";
import {
  AuthStackParamList,
  BottomTabsStackParamList,
  HomeStackParamList,
  RootStackParamList,
} from "./types";

export type RootStackNavigationProp =
  NativeStackNavigationProp<RootStackParamList>;

export type AuthStackNavigationProp =
  NativeStackNavigationProp<AuthStackParamList>;

export type HomeStackNavigationProp =
  NativeStackNavigationProp<HomeStackParamList>;

export type BottomTabsNavigationProp =
  NativeStackNavigationProp<BottomTabsStackParamList>;
