import React from "react";
import { Pressable, StyleSheet, View, type ViewProps } from "react-native";
import type { AnimatedProps } from "react-native-reanimated";
import Animated from "react-native-reanimated";
import { Image } from "expo-image";
import { Bell, Check, Clock, Tag } from "lucide-react-native";
import { TaskItem } from "@/features/tasks/types";
import { LinearGradient } from "expo-linear-gradient";
import ThemeText from "@/components/ThemeText";

interface Props extends AnimatedProps<ViewProps> {
  task: TaskItem;
  onComplete?: (task: TaskItem) => void;
}

export const HomeSlideItem: React.FC<Props> = ({ task, onComplete }) => {
  const uri = task?.image_url;
  const due = task?.due_at
    ? new Date(task.due_at).toLocaleString(undefined, {
        day: "numeric",
        month: "short",
        hour: "numeric",
        minute: "2-digit",
      })
    : "No due date";

  return (
    <Animated.View className="flex-1 overflow-hidden justify-end mx-15">
      <View className="flex-1 overflow-hidden rounded-[25px] bg-ink p-5 justify-end">
        <Image
          style={StyleSheet.absoluteFill}
          source={{ uri }}
          contentFit="cover"
        />

        <View className="absolute right-5 top-5 h-12 w-12 items-center justify-center rounded-full bg-canvas/25">
          <Bell size={20} color="white" />
        </View>

        <View className="">
          <ThemeText
            variant="cardTitle"
            numberOfLines={1}
            className="font-bold text-white"
          >
            {task?.title}
          </ThemeText>
          <ThemeText
            variant="cardDescription"
            className="capitalize text-white/60"
          >
            {task?.status}
          </ThemeText>

          <View className="mt-4 flex-row items-center gap-5">
            <View className="flex-row items-center gap-2">
              <Tag size={18} color="white" />
              <ThemeText className="text-base capitalize text-white">
                {task?.priority}
              </ThemeText>
            </View>
            <View className="flex-row items-center gap-2">
              <Clock size={18} color="white" />
              <ThemeText className="text-base text-white">{due}</ThemeText>
            </View>
          </View>

          <Pressable
            onPress={() => onComplete?.(task)}
            className="mt-5 h-14 flex-row items-center justify-center gap-2 rounded-full bg-white"
          >
            <Check size={18} color="black" />
            <ThemeText className="text-base font-semibold text-black">
              Mark as done
            </ThemeText>
          </Pressable>
        </View>
      </View>
    </Animated.View>
  );
};
