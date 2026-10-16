import { Pressable, View } from "react-native";
import { useNavigation } from "@react-navigation/native";
import { themeColors } from "@/theme";
import { ChevronLeft } from "lucide-react-native";

type BackButtonVariant = "light" | "dark";

type BackButtonProps = {
  variant?: BackButtonVariant;
  goBack?: boolean;
  onPress?: any;
};

const variantClasses: Record<BackButtonVariant, string> = {
  light: "border-canvas",
  dark: "border-steel",
};

const BackButton = (props: BackButtonProps) => {
  const navigation = useNavigation();
  function clickHandler() {
    navigation.goBack();
  }

  return (
    <Pressable
      onPress={() => {
        props?.goBack && clickHandler();
        props?.onPress();
      }}
      className="z-999 rounded-default shadow-sm"
      hitSlop={15}
    >
      <View
        className={`h-10 w-10 items-center justify-center rounded-default border ${variantClasses[props?.variant ?? "dark"]}`}
      >
        <ChevronLeft
          stroke={
            props?.variant === "dark" ? themeColors?.steel : themeColors?.canvas
          }
          height={25}
          width={25}
          strokeWidth={1.5}
        />
      </View>
    </Pressable>
  );
};

export default BackButton;
