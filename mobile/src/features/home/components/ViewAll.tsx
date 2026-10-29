import React from "react";
import { Pressable } from "react-native";
import {
  ArrowRight,
  ArrowRightCircle,
  ChevronRight,
} from "lucide-react-native";
import ThemeText from "@/components/ThemeText";
import { BottomTabsNavigationProp } from "@/navigation/routes";
import { useNavigation } from "@react-navigation/native";

export const ViewAll: React.FC = () => {
  const navigation = useNavigation<BottomTabsNavigationProp>();

  return (
    <Pressable
      onPress={() => navigation.navigate("Tasks")}
      hitSlop={8}
      accessibilityRole="button"
      accessibilityLabel="View all tasks"
      className="flex-1 w-full self-center flex-row items-center gap-1 rounded-full p-5"
    >
      <ThemeText className="text-xs text-canvas">View all</ThemeText>
      <ArrowRight size={16} color="white" />
    </Pressable>
  );
};
