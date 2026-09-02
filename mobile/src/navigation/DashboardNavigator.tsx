import React from "react";
import { createNativeStackNavigator } from "@react-navigation/native-stack";
import { useAppSelector } from "@/app/store";
import OnboardingQuestionnaire from "@/features/onboarding/screens/OnboardingQuestionnaire";
// import ProfileCompletionScreen from "@/features/onboarding/screens/ProfileCompletionScreen";
import Home from "@/features/home/screens/Home";
import ProfileDetailsPending from "@/features/profile/screens/ProfileDetailsPending";

const Stack = createNativeStackNavigator();

const DashboardNavigator = () => {
  const userProfile = useAppSelector((state) => state?.userProfile);

  if (!userProfile?.is_onboarding_completed) {
    return <OnboardingQuestionnaire />;
  }

  if (!userProfile?.is_profile_completed) {
    return <ProfileDetailsPending />;
  }

  return (
    <Stack.Navigator
      id="dashboard-navigator"
      screenOptions={{
        gestureEnabled: true,
        fullScreenGestureEnabled: true,
        headerShown: false,
        animation: "ios_from_right",
      }}
    >
      <Stack.Screen name="Home" component={Home} />
    </Stack.Navigator>
  );
};

export default DashboardNavigator;
