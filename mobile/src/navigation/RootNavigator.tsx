import { StyleSheet, Text, View } from "react-native";
import React, { useEffect } from "react";
import { createNativeStackNavigator } from "@react-navigation/native-stack";
import { useAwakeServerCall } from "@/hooks/useAwakeServer";
import OnboardingCarousel from "../features/onboarding/screens/OnboardingCarousel";
import Register from "../features/auth/screens/Register";
import Login from "../features/auth/screens/Login";

const Stack = createNativeStackNavigator();
const RootNavigator = () => {
  const callAwakeServer = useAwakeServerCall();

  useEffect(() => {
    callAwakeServer();
  }, []);

  return (
    <Stack.Navigator
      id="root-navigator"
      initialRouteName="OnboardingCarousel"
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
      {/* <Stack.Screen name="Dashboard" component={DrawerNavigator} /> */}
    </Stack.Navigator>
  );
};

export default RootNavigator;
