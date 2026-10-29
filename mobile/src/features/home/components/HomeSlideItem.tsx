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
        <View className="flex-1 overflow-hidden bg-ink justify-end rounded-[35px] border-mist border-6 shadow-xl">
          <Image
            style={StyleSheet.absoluteFill}
            source={{ uri }}
            contentFit="cover"
          />
          <LinearGradient
            colors={[
              "rgba(0,0,0,0)",
              "rgba(0,0,0,0)",
              "rgba(18,18,18,0.2)",
              "rgba(58,58,58,0.4)",
              "rgba(0,0,0,0.75)",
            ]}
            locations={[0, 0.75, 0.85, 0.95, 1]}
            pointerEvents="none"
            start={{ x: 0.5, y: 0 }}
            end={{ x: 0.5, y: 1 }}
            className="absolute inset-0"
            style={{ zIndex: 10 }}
          />

          {/* <View className="absolute right-5 top-5 h-10 w-10 items-center justify-center rounded-full bg-canvas/25">
            <X size={22.5} color={themeColors?.canvas} />
          </View> */}

          <View className="p-5 pt-0 z-20 gap-2">
            <ThemeText
              variant="cardTitle"
              numberOfLines={1}
              className="font-bold text-canvas capitalize"
            >
              {task?.title}
            </ThemeText>
            <ThemeText variant="cardDescription" className="text-cloud">
              {statusLabels[task?.status] ?? task?.status}
            </ThemeText>

            <View className="mt-4 flex-row items-center gap-5">
              <View className="flex-row items-center gap-2">
                <Tag size={18} color={themeColors?.mist} />
                <ThemeText className="text-base capitalize text-mist">
                  {priorityLabels[task?.priority] ?? task?.priority}
                </ThemeText>
              </View>
              <View className="flex-row items-center gap-2">
                <Clock size={18} color={themeColors?.mist} />
                <ThemeText className="text-base text-mist capitalize">
                  {due}
                </ThemeText>
              </View>
            </View>

            {/* <Pressable
              onPress={() => onComplete?.(task)}
              className="mt-5 h-14 flex-row items-center justify-center gap-2 rounded-full bg-canvas"
            >
              <Check size={18} color="black" />
              <ThemeText className="text-base font-semibold text-black">
                Mark as done
              </ThemeText>
            </Pressable> */}
          </View>
        </View>
      )}
    </Animated.View>
  );
};
