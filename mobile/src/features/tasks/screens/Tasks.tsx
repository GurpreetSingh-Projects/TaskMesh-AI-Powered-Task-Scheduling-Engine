import { ScrollView, View, Pressable } from "react-native";
import { ChevronRight } from "lucide-react-native";
import ThemePage from "@/components/ThemePage";
import ThemePageHeader from "@/components/ThemePageHeader";
import ThemeText from "@/components/ThemeText";
import { themeColors } from "@/theme";
import Category from "../components/Category";
import { TaskCategory } from "../types";
import { statusLabels, TASK_STATUS } from "../utils";

export const TASK_CATEGORIES: TaskCategory[] = [
  {
    status: TASK_STATUS[0],
    title: "Overdue",
    description: "Past their due date. Tackle these first.",
    view_more: "/tasks/overdue",
  },
  {
    status: TASK_STATUS[1],
    title: "In Progress",
    description: "Already started. Keep the momentum going.",
    view_more: "/tasks/in_progress",
  },
  {
    status: TASK_STATUS[2],
    title: "Pending",
    description: "Waiting for you to get started.",
    view_more: "/tasks/pending",
  },
  {
    status: TASK_STATUS[3],
    title: "Recently Completed",
    description: "Done and dusted. Nice work.",
    view_more: "/tasks/completed",
  },
];

const Tasks = () => {
  return (
    <ThemePage>
      <ThemePageHeader heading="Tasks" backMode />
      <ScrollView
        showsVerticalScrollIndicator={false}
        contentContainerClassName="py-page gap-section pb-8"
        className="gap-5"
      >
        {TASK_CATEGORIES?.map((item, index) => (
          <Category key={index} category={item} />
        ))}
      </ScrollView>
    </ThemePage>
  );
};

export default Tasks;
