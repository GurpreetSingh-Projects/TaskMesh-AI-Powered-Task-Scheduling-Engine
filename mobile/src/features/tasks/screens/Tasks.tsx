import { ScrollView, StyleSheet, View } from "react-native";
import ThemePage from "@/components/ThemePage";
import ThemePageHeader from "@/components/ThemePageHeader";

const Tasks = () => {
  return (
    <ThemePage>
      <ThemePageHeader heading="Tasks" />
      <ScrollView contentContainerClassName="flex-1"></ScrollView>
    </ThemePage>
  );
};

export default Tasks;

const styles = StyleSheet.create({});
