import type { NativeStackNavigationProp } from "@react-navigation/native-stack";
import {
  AuthStackParamList,
  BottomTabsStackParamList,
  DashboardStackParamList,
  RootStackParamList,
} from "./types";
import { BottomTabNavigationProp } from "@react-navigation/bottom-tabs";
import { CompositeNavigationProp } from "@react-navigation/native";

export type RootStackNavigationProp =
  NativeStackNavigationProp<RootStackParamList>;

export type AuthStackNavigationProp =
  NativeStackNavigationProp<AuthStackParamList>;

export type DashboardStackNavigationProp =
  NativeStackNavigationProp<DashboardStackParamList>;

export type BottomTabsNavigationProp =
  BottomTabNavigationProp<BottomTabsStackParamList>;

export type HomeStackNavigationProp = CompositeNavigationProp<
  DashboardStackNavigationProp,
  BottomTabsNavigationProp
>;
