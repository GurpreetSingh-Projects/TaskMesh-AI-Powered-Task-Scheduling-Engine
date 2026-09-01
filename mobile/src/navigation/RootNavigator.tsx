import { StyleSheet, Text, View } from "react-native";
import React, { useEffect } from "react";
import { createNativeStackNavigator } from "@react-navigation/native-stack";
import { useAwakeServerCall } from "@/hooks/useAwakeServer";
import Register from "../features/auth/screens/Register";
import Login from "../features/auth/screens/Login";
import { useAppSelector } from "@/app/store";
import OnboardingCarousel from "@/features/onboarding/screens/OnboardingCarousel";
import OnboardingQuestionnaire from "@/features/onboarding/screens/OnboardingQuestionnaire";
import Home from "@/features/home/screens/Home";

const Stack = createNativeStackNavigator();
const RootNavigator = () => {
  const callAwakeServer = useAwakeServerCall();

  const settings = useAppSelector((state) => state?.settings);
  const userProfile = useAppSelector((state) => state?.userProfile);

  console.log("User", userProfile);
  console.log("Settings", settings);

  const getInitialRoute = () => {
    return userProfile?.user_id
      ? "OnboardingQuestionnaire"
      : "OnboardingCarousel";
  };

  useEffect(() => {
    callAwakeServer();
  }, []);

  return (
    <Stack.Navigator
      id="root-navigator"
      initialRouteName={getInitialRoute()}
      screenOptions={{
        gestureEnabled: true,
        fullScreenGestureEnabled: true,
        headerShown: false,
        animation: "ios_from_right",
      }}
    >
      <Stack.Screen name="OnboardingCarousel" component={OnboardingCarousel} />
      <Stack.Screen name="Login" component={Login} />
      <Stack.Screen name="Register" component={Register} />
      <Stack.Screen
        name="OnboardingQuestionnaire"
        component={OnboardingQuestionnaire}
      />
      <Stack.Screen name="Home" component={Home} />
      {/* <Stack.Screen name="Dashboard" component={DrawerNavigator} /> */}
    </Stack.Navigator>
  );
};

export default RootNavigator;
