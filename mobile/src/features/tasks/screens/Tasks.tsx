import { ScrollView, View, Pressable } from "react-native";
import { ChevronRight } from "lucide-react-native";
import ThemePage from "@/components/ThemePage";
import ThemePageHeader from "@/components/ThemePageHeader";
import ThemeText from "@/components/ThemeText";
import { themeColors } from "@/theme";

const Tasks = () => {
  return (
    <ThemePage>
      <ThemePageHeader heading="Tasks" />

      <ScrollView
        showsVerticalScrollIndicator={false}
        contentContainerClassName="p-page gap-section pb-8"
      >
        {/* Overdue Tasks */}
        <View className="gap-subsection">
          <Pressable className="flex-row items-center justify-between">
            <View className="gap-1">
              <ThemeText variant="sectionTitle">Overdue Tasks</ThemeText>
              <ThemeText variant="sectionSubtitle">
                Tasks that passed their due date.
              </ThemeText>
            </View>

            <Pressable className="h-11 w-11 items-center justify-center rounded-full bg-mist">
              <ChevronRight size={25} color={themeColors?.smoke} />
            </Pressable>
          </Pressable>
        </View>

        {/* Pending Tasks */}
        <View className="gap-subsection">
          <Pressable className="flex-row items-center justify-between">
            <View className="gap-1">
              <ThemeText variant="sectionTitle">Pending Tasks</ThemeText>
              <ThemeText variant="sectionSubtitle">
                Tasks waiting to be started.
              </ThemeText>
            </View>

            <Pressable className="h-11 w-11 items-center justify-center rounded-full bg-mist">
              <ChevronRight size={25} color={themeColors?.smoke} />
            </Pressable>
          </Pressable>
        </View>

        {/* In Progress */}
        <View className="gap-subsection">
          <Pressable className="flex-row items-center justify-between">
            <View className="gap-1">
              <ThemeText variant="sectionTitle">In Progress</ThemeText>
              <ThemeText variant="sectionSubtitle">
                Tasks currently being worked on.
              </ThemeText>
            </View>

            <Pressable className="h-11 w-11 items-center justify-center rounded-full bg-mist">
              <ChevronRight size={25} color={themeColors?.smoke} />
            </Pressable>
          </Pressable>
        </View>

        {/* Recently Completed */}
        <View className="gap-subsection">
          <Pressable className="flex-row items-center justify-between">
            <View className="gap-1">
              <ThemeText variant="sectionTitle">Recently Completed</ThemeText>
              <ThemeText variant="sectionSubtitle">
                Tasks you have finished recently.
              </ThemeText>
            </View>

            <Pressable className="h-11 w-11 items-center justify-center rounded-full bg-mist">
              <ChevronRight size={25} color={themeColors?.smoke} />
            </Pressable>
          </Pressable>
        </View>
      </ScrollView>
    </ThemePage>
  );
};

export default Tasks;
