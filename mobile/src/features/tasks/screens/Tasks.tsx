import { ScrollView, View, Pressable } from "react-native";
import { ChevronRight } from "lucide-react-native";
import ThemePage from "@/components/ThemePage";
import ThemePageHeader from "@/components/ThemePageHeader";
import ThemeText from "@/components/ThemeText";
import { themeColors } from "@/theme";
import Category from "../components/Category";
import { TaskCategory } from "../types";
import { statusLabels } from "../utils";

export const TASK_CATEGORIES: TaskCategory[] = [
  {
    status: statusLabels.OVERDUE,
    title: "Overdue",
    description: "Past their due date. Tackle these first.",
    view_more: "/tasks/overdue",
  },
  {
    status: statusLabels.IN_PROGRESS,
    title: "In Progress",
    description: "Already started. Keep the momentum going.",
    view_more: "/tasks/in_progress",
  },
  {
    status: statusLabels.PENDING,
    title: "Pending",
    description: "Waiting for you to get started.",
    view_more: "/tasks/pending",
  },
  {
    status: statusLabels.COMPLETED,
    title: "Completed",
    description: "Done and dusted. Nice work.",
    view_more: "/tasks/completed",
  },
];

const Tasks = () => {
  return (
    <ThemePage>
      <ThemePageHeader heading="Tasks" />

      <ScrollView
        showsVerticalScrollIndicator={false}
        contentContainerClassName="p-page gap-section pb-8"
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
