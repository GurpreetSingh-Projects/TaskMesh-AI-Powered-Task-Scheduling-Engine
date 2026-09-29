import { Pressable, View } from "react-native";
import { useNavigation } from "@react-navigation/native";
import { themeColors } from "@/theme";
import { ChevronLeft } from "lucide-react-native";

const BackButton = (props) => {
  const navigation = useNavigation();
  function clickHandler() {
    navigation.goBack();
  }
  return (
    <Pressable
      onPress={() => {
        props?.goBack && clickHandler();
      }}
      className="shadow-sm z-999 rounded-default"
      hitSlop={15}
    >
      <View className="items-center justify-center h-11.5 w-11.5 rounded-full">
        <ChevronLeft
          stroke={themeColors?.ink}
          height={20}
          width={20}
          strokeWidth={1.5}
        />
      </View>
    </Pressable>
  );
};

export default BackButton;
