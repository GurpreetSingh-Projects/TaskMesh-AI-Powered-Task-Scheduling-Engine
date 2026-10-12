import { Pressable, View } from "react-native";
import ThemeText from "./ThemeText";

type ThemeTabGroupProps = {
  value: any;
  onChange: (value: any) => void;
  options: any;
};

const ThemeTabGroup = (props: ThemeTabGroupProps) => {
  return (
    <View className="w-full flex-row rounded-xl bg-ash p-1">
      {props?.options?.map((option) => {
        const selected = option?.value === props?.value;
        return (
          <Pressable
            key={String(option?.value)}
            onPress={() => props?.onChange(option?.value)}
            className={`flex-1 items-center justify-center rounded-full p-2.5 ${
              selected ? "bg-ink" : ""
            }`}
          >
            <ThemeText
              className={`text-xs! ${
                selected ? "font-medium text-canvas" : "text-mist"
              }`}
            >
              {option?.label}
            </ThemeText>
          </Pressable>
        );
      })}
    </View>
  );
};

export default ThemeTabGroup;
