import { Image, Pressable, Text, View } from "react-native";
import { Ionicons } from "@expo/vector-icons";

type Props = {
  title: string;
  status: string; // "Pending"
  priority: string; // "Normal"
  timeAgo: string; // "18 Minutes Ago"
  imageUri?: string;
  onDone: () => void;
  onSecondary?: () => void;
};

export function TaskCard({
  title,
  status,
  priority,
  timeAgo,
  imageUri,
  onDone,
  onSecondary,
}: Props) {
  return (
    <View
      className="w-[300px] rounded-[36px] bg-white p-2.5"
      style={{
        shadowColor: "#000",
        shadowOpacity: 0.12,
        shadowRadius: 24,
        shadowOffset: { width: 0, height: 12 },
        elevation: 10,
      }}
    >
      {/* image */}
      <View className="h-[340px] overflow-hidden rounded-[30px] bg-neutral-200">
        {imageUri ? (
          <Image
            source={{ uri: imageUri }}
            className="h-full w-full"
            resizeMode="cover"
          />
        ) : null}
      </View>

      {/* text */}
      <View className="px-3 pt-4">
        <Text
          numberOfLines={1}
          className="text-[28px] font-semibold tracking-tight text-black"
        >
          {title}
        </Text>
        <Text className="mt-0.5 text-base text-neutral-400">{status}</Text>

        <View className="mt-4 flex-row items-center">
          <Ionicons name="pricetag-outline" size={18} color="#9ca3af" />
          <Text className="ml-2 text-base font-semibold text-black">
            {priority}
          </Text>
          <Ionicons
            name="time-outline"
            size={18}
            color="#9ca3af"
            style={{ marginLeft: 20 }}
          />
          <Text className="ml-2 text-base font-semibold text-black">
            {timeAgo}
          </Text>
        </View>

        {/* actions */}
        <View className="mb-2 mt-5 flex-row items-center">
          <Pressable
            onPress={onDone}
            className="h-[52px] flex-1 items-center justify-center rounded-full bg-black active:opacity-80"
          >
            <Text className="text-base font-semibold text-white">
              Mark as done
            </Text>
          </Pressable>
          <Pressable
            onPress={onSecondary}
            className="ml-3 h-[52px] w-[52px] items-center justify-center rounded-full border border-neutral-200 bg-white active:opacity-70"
          >
            <Ionicons name="heart-outline" size={22} color="#ef4444" />
          </Pressable>
        </View>
      </View>
    </View>
  );
}
