import { createNativeStackNavigator } from "@react-navigation/native-stack";
import { useAppSelector } from "@/app/store";
import OnboardingQuestionnaire from "@/features/onboarding/screens/OnboardingQuestionnaire";
import Home from "@/features/home/screens/Home";
import ProfileDetailsPending from "@/features/profile/screens/ProfileDetailsPending";
import { useRefreshToken } from "@/hooks/useRefreshToken";
import { useEffect } from "react";
import { useNavigation } from "@react-navigation/native";
import { HomeStackParamList } from "./types";

const Stack = createNativeStackNavigator<HomeStackParamList>();

const DashboardNavigator = () => {
  const user = useAppSelector((state) => state?.user);
  const navigation = useNavigation();
  const refreshToken = useRefreshToken();

  useEffect(() => {
    refreshToken();
  }, []);

  if (!user?.is_onboarding_completed) {
    return <OnboardingQuestionnaire />;
  }

  if (!user?.is_profile_completed) {
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
      <Stack.Screen
        name="OnboardingQuestionnaire"
        component={OnboardingQuestionnaire}
      />
      <Stack.Screen
        name="ProfileDetailsPending"
        component={ProfileDetailsPending}
      />
      <Stack.Screen name="Home" component={Home} />
    </Stack.Navigator>
  );
};

export default DashboardNavigator;
