import { Animated, Pressable, View } from "react-native";
import { TaskCategory } from "../types";
import ThemeText from "@/components/ThemeText";
import { ChevronRight } from "lucide-react-native";
import { themeColors } from "@/theme";
import { useGetTasksQuery } from "../taskApi";
import LottieView from "lottie-react-native";
import { animations } from "@/assets";
import { FlatList } from "react-native-gesture-handler";
import TaskCard from "./TaskCard";
import { useFocusEffect } from "@react-navigation/native";
import { useCallback } from "react";

type Props = {
  category: TaskCategory;
};

const Category = ({ category }: Props) => {
  const {
    // getTasks,
    refetch: refetchTasks,
    data: tasksData,
    isLoading: areTasksLoading,
    isError: areTasksError,
    error: tasksError,
  } = useGetTasksQuery({
    status: category?.status,
    limit: 5,
  });

  // console.log(tasksData?.items);
  useFocusEffect(
    useCallback(() => {
      refetchTasks();
    }, [refetchTasks]),
  );
  return (
    <View>
      <View
        // onPress={() => router.push(category?.view_more)}
        className="flex-row items-center px-page"
      >
        <View className="flex-1 gap-1">
          <ThemeText variant="sectionTitle">{category?.title}</ThemeText>
          <ThemeText variant="sectionSubtitle">
            {category?.description}
          </ThemeText>
        </View>
        <Pressable className="items-center justify-center p-1.5 rounded-full bg-mist">
          <ChevronRight size={25} color={themeColors?.smoke} />
        </Pressable>
      </View>
      <View className="flex-row items-center gap-3">
        {areTasksLoading ? (
          <Animated.View
            // entering={FadeInUp}
            // exiting={FadeOutDown}
            className="items-center justify-center py-5 w-full"
          >
            <LottieView
              source={animations?.loadingIcon}
              autoPlay
              loop
              style={{
                width: 50,
                height: 50,
                backgroundColor: themeColors?.steel,
              }}
            />
          </Animated.View>
        ) : tasksData?.items?.length ? (
          <FlatList
            horizontal
            data={tasksData?.items}
            keyExtractor={(item) => item?.task_id}
            renderItem={({ item }) => <TaskCard {...item} />}
            ItemSeparatorComponent={() => <View className="w-4" />}
          />
        ) : (
          <View className="w-full items-center justify-center py-10">
            <ThemeText className="text-sm text-cloud">No tasks found</ThemeText>
          </View>
        )}
      </View>
    </View>
  );
};

export default Category;
