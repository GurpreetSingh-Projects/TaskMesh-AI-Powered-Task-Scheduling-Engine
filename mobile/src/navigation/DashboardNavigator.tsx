import { createNativeStackNavigator } from "@react-navigation/native-stack";
import OnboardingQuestionnaire from "@/features/onboarding/screens/OnboardingQuestionnaire";
import Home from "@/features/home/screens/Home";
import ProfileDetailsPending from "@/features/profile/screens/ProfileDetailsPending";
import { useRefreshToken } from "@/hooks/useRefreshToken";
import { useEffect } from "react";
import { HomeStackParamList } from "./types";
import { useAppSelector } from "@/app/store";
import BottomTabs from "./BottomTabs";
import LabelManagement from "@/features/labels/screens/LabelManagement";
import Settings from "@/features/home/screens/Settings";

const Stack = createNativeStackNavigator<HomeStackParamList>();

const DashboardNavigator = () => {
  const user = useAppSelector((state) => state?.user);
  const refreshToken = useRefreshToken();

  useEffect(() => {
    refreshToken();
  }, []);

  if (!user.is_onboarding_completed) return <OnboardingQuestionnaire />;
  if (!user.is_profile_completed && !user.isProfileCompletionSkipped)
    return <ProfileDetailsPending />;

  return (
    <Stack.Navigator
      id="dashboard-navigator"
      initialRouteName="BottomTabs"
      screenOptions={{
        gestureEnabled: true,
        fullScreenGestureEnabled: true,
        headerShown: false,
        animation: "ios_from_right",
      }}
    >
      <Stack.Screen
        name="OnboardingQuestionnaire"
        component={OnboardingQuestionnaire}
      />
      <Stack.Screen
        name="ProfileDetailsPending"
        component={ProfileDetailsPending}
      />
      <Stack.Screen name="BottomTabs" component={BottomTabs} />
      <Stack.Screen name="LabelManagement" component={LabelManagement} />
      <Stack.Screen name="Settings" component={Settings} />
    </Stack.Navigator>
  );
};

export default DashboardNavigator;
