import { Platform, useWindowDimensions, View } from "react-native";
import BackButton from "./BackButton";
import ThemeText from "./ThemeText";

type PageHeaderProps = {
  heading?: string;
  background?: string;
  editMode?: boolean;
  backMode?: boolean;
};

const ThemePageHeader = (props: PageHeaderProps) => {
  const { height, width } = useWindowDimensions();
  return (
    <View className="w-full">
      <View className="absolute left-0 p-3 top-[12.5%]">
        <BackButton goBack />
      </View>
      <View className="items-center">
        <ThemeText
          variant="heading"
          className="text-lg opacity-55 max-w-[72%] truncate"
          numberOfLines={1}
        >
          {props?.heading ? props?.heading : ""}
        </ThemeText>
      </View>
      <View></View>
    </View>
  );
};

export default ThemePageHeader;
