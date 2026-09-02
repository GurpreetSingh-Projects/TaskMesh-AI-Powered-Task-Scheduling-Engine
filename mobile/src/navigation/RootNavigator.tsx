import { useEffect } from "react";
import { createNativeStackNavigator } from "@react-navigation/native-stack";
import { useAwakeServerCall } from "@/hooks/useAwakeServer";
import { useAppSelector } from "@/app/store";
import DashboardNavigator from "./DashboardNavigator";
import AuthNavigator from "./AuthNavigator";

const Stack = createNativeStackNavigator();

const RootNavigator = () => {
  const callAwakeServer = useAwakeServerCall();
  const auth = useAppSelector((state) => state?.auth);

  useEffect(() => {
    callAwakeServer();
  }, []);

  return (
    <Stack.Navigator
      id="root-navigator"
      screenOptions={{ headerShown: false, animation: "fade" }}
    >
      <Stack.Screen
        name={auth?.isAuthenticated ? "Dashboard" : "Auth"}
        component={auth?.isAuthenticated ? DashboardNavigator : AuthNavigator}
      />
    </Stack.Navigator>
  );
};

export default RootNavigator;
