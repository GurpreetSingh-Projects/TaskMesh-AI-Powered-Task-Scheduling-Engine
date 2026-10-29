import Home from "@/features/home/screens/Home";
import { createBottomTabNavigator } from "@react-navigation/bottom-tabs";
import { BottomTabsStackParamList } from "./types";
import Tasks from "@/features/tasks/screens/Tasks";
import Profile from "@/features/profile/screens/Profile";
import Notifications from "@/features/notifications/screens/Notifications";
import { Pressable, View } from "react-native";
import { ListTodo, Bell, HomeIcon, UserRound, Plus } from "lucide-react-native";
import { themeColors } from "@/theme";
import { useRef } from "react";
import ThemeText from "@/components/ThemeText";
import CreateTask from "@/features/tasks/screens/CreateTask";

const Tab = createBottomTabNavigator<BottomTabsStackParamList>();

const TabIcon = {
  Home: HomeIcon,
  Tasks: ListTodo,
  CreateTask: Plus,
  Notifications: Bell,
  Profile: UserRound,
} as const;

const BottomTabs = () => {
  const targetRef = useRef(null);
  return (
    <Tab.Navigator
      id="bottom-tabs-navigator"
      initialRouteName="Home"
      screenOptions={({ route }) => ({
        headerShown: false,
        tabBarActiveTintColor: themeColors?.canvas,
        tabBarInactiveTintColor: themeColors?.cloud,
        tabBarLabelStyle: {
          fontSize: 12,
          fontWeight: "600",
        },
        tabBarIconStyle: {
          height: 16,
          width: 16,
        },
        tabBarStyle: {
          position: "absolute",
          bottom: 24,
          height: 64,
          paddingHorizontal: 25,
          paddingVertical: 25,
          marginHorizontal: 35,
          borderRadius: 9999,
          backgroundColor: `${themeColors?.ink}75`,
          borderTopWidth: 0,
          shadowColor: themeColors?.ink,
          shadowOpacity: 0.12,
          shadowRadius: 12,
          shadowOffset: {
            width: 0,
            height: 4,
          },
          elevation: 4,
        },
        tabBarItemStyle: {
          alignItems: "center",
          justifyContent: "center",
        },
        tabBarIcon: ({ color, focused }) => {
          const Icon = TabIcon?.[route.name];

          return (
            <View className="rounded-full">
              <Icon
                size={25}
                color={focused ? themeColors?.mist : color}
                strokeWidth={2}
              />
            </View>
          );
        },
        tabBarButton: ({ ref, ...props }) => (
          <Pressable
            {...props}
            className="items-center justify-center rounded-full p-3 gap-1"
            style={[
              {
                backgroundColor: props?.accessibilityState?.selected
                  ? `${themeColors?.canvas}90`
                  : "transparent",
              },
            ]}
            hitSlop={15}
          />
        ),
        tabBarLabel: () => null,
        tabBarHideOnKeyboard: true,
        lazy: true,
        freezeOnBlur: true,
      })}
    >
      <Tab.Screen name="Home" component={Home} />
      <Tab.Screen name="Tasks" component={Tasks} />
      <Tab.Screen
        name="CreateTask"
        component={CreateTask}
        options={{
          tabBarLabel: () => null,
          tabBarIcon: () => {
            return (
              <View className="rounded-full items-center justify-center h-12.5 w-12.5 bg-ink">
                <Plus color={themeColors?.canvas} strokeWidth={2} size={30} />
              </View>
            );
          },
        }}
      />
      <Tab.Screen name="Notifications" component={Notifications} />
      <Tab.Screen name="Profile" component={Profile} />
    </Tab.Navigator>
  );
};

export default BottomTabs;
