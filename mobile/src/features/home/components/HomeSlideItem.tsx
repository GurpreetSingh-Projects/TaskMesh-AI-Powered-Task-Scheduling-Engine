import React from "react";
import {
  Pressable,
  StyleSheet,
  Text,
  View,
  type ViewProps,
} from "react-native";
import type { AnimatedProps } from "react-native-reanimated";
import Animated from "react-native-reanimated";
import { Image } from "expo-image";
import { Bell, Check, Clock, Tag } from "lucide-react-native";
import { TaskItem } from "@/features/tasks/types";
import { LinearGradient } from "expo-linear-gradient";
import { BlurView } from "expo-blur";

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
    <Animated.View className="flex-1 overflow-hidden rounded-[50px]">
      <Image
        style={StyleSheet.absoluteFill}
        source={{ uri }}
        contentFit="cover"
        blurRadius={60}
      />

      <View className="flex-1 p-5">
        <View className="flex-1 overflow-hidden rounded-[50px] bg-ink">
          {/* <LinearGradient
            colors={[
              "rgba(0,0,0,0)",
              "rgba(0,0,0,0)",
              "rgba(3,3,3,0.08)",
              "rgba(7,7,7,0.18)",
              "rgba(18,18,18,0.32)",
              "rgba(26,26,26,0.48)",
              "rgba(36,36,36,0.64)",
              "rgba(58,58,58,0.82)",
              "#000000",
            ]}
            locations={[0, 0.6, 0.65, 0.71, 0.78, 0.85, 0.91, 0.96, 1]}
            pointerEvents="none"
            start={{ x: 0.5, y: 0 }}
            end={{ x: 0.5, y: 1 }}
            className="absolute inset-0"
            style={{ zIndex: -1 }}
          /> */}

          <Image
            style={StyleSheet.absoluteFill}
            source={{ uri }}
            contentFit="cover"
          />

          <View className="absolute right-5 top-5 h-12 w-12 items-center justify-center rounded-full bg-canvas/25">
            <Bell size={20} color="white" />
          </View>
          <View className="flex-1 justify-end p-5">
            <View className="">
              <BlurView
                intensity={100}
                className="absolute inset-0"
                pointerEvents="none"
              />
              <Text numberOfLines={1} className="text-4xl font-bold text-white">
                {task?.title}
              </Text>
              <Text className="mt-1 text-lg capitalize text-white/60">
                {task?.status}
              </Text>

              <View className="mt-4 flex-row items-center gap-5">
                <View className="flex-row items-center gap-2">
                  <Tag size={18} color="white" />
                  <Text className="text-base capitalize text-white">
                    {task?.priority}
                  </Text>
                </View>
                <View className="flex-row items-center gap-2">
                  <Clock size={18} color="white" />
                  <Text className="text-base text-white">{due}</Text>
                </View>
              </View>

              <Pressable
                onPress={() => onComplete?.(task)}
                className="mt-5 h-14 flex-row items-center justify-center gap-2 rounded-full bg-white"
              >
                <Check size={18} color="black" />
                <Text className="text-base font-semibold text-black">
                  Mark as done
                </Text>
              </Pressable>
            </View>
          </View>
        </View>
      </View>
    </Animated.View>
  );
};
