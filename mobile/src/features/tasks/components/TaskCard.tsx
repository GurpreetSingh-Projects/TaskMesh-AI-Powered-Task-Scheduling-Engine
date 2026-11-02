import { Image, Text, View } from "react-native";
import { Clock, Flag, CheckCircle2, Tag } from "lucide-react-native";
import type { TaskItem } from "@/features/tasks/types";
import { themeColors } from "@/theme";
import ThemeText from "@/components/ThemeText";
import { priorityLabels, statusLabels } from "../utils";
import { timeLeft } from "@/utils";

export default function TaskCard(task: TaskItem) {
  const due = timeLeft(task?.due_at);

  return (
    <View className="w-65 h-100 my-3 overflow-hidden rounded-[35px] border border-neutral-200 bg-white shadow-lg">
      <View className="p-3 h-[65%]">
        {task.image_url ? (
          <Image
            source={{ uri: task.image_url }}
            className="flex-1 rounded-[35px]"
            resizeMode="cover"
          />
        ) : (
          <View className="w-full items-center justify-center bg-neutral-100">
            <Text className="text-sm text-neutral-400">No image available</Text>
          </View>
        )}
      </View>

      <View className="px-5 pt-2 z-20 gap-0.5">
        <ThemeText
          variant="cardTitle"
          numberOfLines={1}
          className="text-lg font-bold text-obsidian capitalize"
        >
          {task?.title}
        </ThemeText>
        <ThemeText variant="cardDescription" className="text-sm text-ash">
          {statusLabels[task?.status] ?? task?.status}
        </ThemeText>

        <View className="pt-2">
          <ThemeText
            variant="cardDescription"
            numberOfLines={2}
            className={`text-xs font-bold capitalize ${
              task?.description ? "text-ash" : "text-steel"
            }`}
          >
            {task?.description ?? "No description found"}
          </ThemeText>
        </View>

        <View className="mt-4 flex-row items-center gap-5">
          <View className="flex-row items-center gap-2">
            <Tag size={18} color={themeColors?.steel} />
            <ThemeText className="text-xs capitalize text-steel">
              {priorityLabels[task?.priority] ?? task?.priority}
            </ThemeText>
          </View>
          <View className="flex-row items-center gap-2">
            <Clock size={18} color={themeColors?.steel} />
            <ThemeText className="text-xs text-steel capitalize">
              {due}
            </ThemeText>
          </View>
        </View>
      </View>
    </View>
  );
}
