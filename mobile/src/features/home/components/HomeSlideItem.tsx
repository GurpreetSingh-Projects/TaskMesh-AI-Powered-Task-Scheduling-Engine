import React from "react";
import { Pressable, StyleSheet, View, type ViewProps } from "react-native";
import type { AnimatedProps } from "react-native-reanimated";
import Animated from "react-native-reanimated";
import { Image } from "expo-image";
import { Bell, Check, Clock, Tag, X } from "lucide-react-native";
import { TaskItem } from "@/features/tasks/types";
import { LinearGradient } from "expo-linear-gradient";
import ThemeText from "@/components/ThemeText";
import { themeColors } from "@/theme";
import { opacity } from "react-native-reanimated/lib/typescript/Colors";
import HomePlaceholder from "./HomePlaceholder";
import {
  priorityLabels,
  statusLabels,
  TASK_STATUS_OPTIONS,
} from "@/features/tasks/utils";
import { getISTTime, timeLeft } from "@/utils";

interface Props extends AnimatedProps<ViewProps> {
  task: TaskItem;
  isLoading?: boolean;
  onComplete?: (task: TaskItem) => void;
}

const pulse = {
  from: {
    opacity: 0.5,
  },
  to: {
    opacity: 0.85,
  },
};

export const HomeSlideItem: React.FC<Props> = ({
  task,
  onComplete,
  isLoading,
}) => {
  const uri = task?.image_url;
  const due = timeLeft(task?.due_at);

  return (
    <Animated.View className="flex-1 overflow-hidden justify-end mx-15 rounded-[35px]">
      {isLoading ? (
        <HomePlaceholder />
      ) : (
        <View className="flex-1 overflow-hidden bg-ink p-5 justify-end rounded-[35px] border-mist border-7 shadow-2xl">
          <Image
            style={StyleSheet.absoluteFill}
            source={{ uri }}
            contentFit="cover"
          />

          {/* <View className="absolute right-5 top-5 h-10 w-10 items-center justify-center rounded-full bg-canvas/25">
            <X size={22.5} color="white" />
          </View> */}

          <View className="">
            <ThemeText
              variant="cardTitle"
              numberOfLines={1}
              className="font-bold text-canvas capitalize"
            >
              {task?.title}
            </ThemeText>
            <ThemeText variant="cardDescription" className="text-canvas">
              {statusLabels[task?.status] ?? task?.status}
            </ThemeText>

            <View className="mt-4 flex-row items-center gap-5">
              <View className="flex-row items-center gap-2">
                <Tag size={18} color="white" />
                <ThemeText className="text-base capitalize text-white">
                  {priorityLabels[task?.priority] ?? task?.priority}
                </ThemeText>
              </View>
              <View className="flex-row items-center gap-2">
                <Clock size={18} color="white" />
                <ThemeText className="text-base text-white capitalize">
                  {due}
                </ThemeText>
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
      )}
    </Animated.View>
  );
};
