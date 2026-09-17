import { createNativeStackNavigator } from "@react-navigation/native-stack";
import Register from "../features/auth/screens/Register";
import Login from "../features/auth/screens/Login";
import OnboardingCarousel from "@/features/onboarding/screens/OnboardingCarousel";
import { AuthStackParamList } from "./types";

const Stack = createNativeStackNavigator<AuthStackParamList>();

const AuthNavigator = () => {
  return (
    <Stack.Navigator
      id="auth-navigator"
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
    </Stack.Navigator>
  );
};

export default AuthNavigator;
