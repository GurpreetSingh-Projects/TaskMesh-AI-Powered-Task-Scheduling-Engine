import { Pressable, View } from "react-native";
import { TaskCategory } from "../types";
import ThemeText from "@/components/ThemeText";
import { ChevronRight } from "lucide-react-native";
import { themeColors } from "@/theme";

type Props = {
  category: TaskCategory;
};

const Category = ({ category }: Props) => {
  return (
    <View className="gap-subsection">
      <Pressable
        // onPress={() => router.push(category?.view_more)}
        className="flex-row items-center justify-between"
      >
        <View className="flex-1 gap-1 pr-3">
          <ThemeText variant="sectionTitle">{category?.title}</ThemeText>
          <ThemeText variant="sectionSubtitle">
            {category?.description}
          </ThemeText>
        </View>

        <View className="items-center justify-center p-1.5 rounded-full bg-mist">
          <ChevronRight size={25} color={themeColors?.smoke} />
        </View>
      </Pressable>
    </View>
  );
};

export default Category;
