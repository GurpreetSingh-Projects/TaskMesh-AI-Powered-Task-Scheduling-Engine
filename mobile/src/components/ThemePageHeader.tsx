import { Platform, useWindowDimensions, View } from "react-native";
import BackButton from "./BackButton";
import ThemeText from "./ThemeText";
import { SectionDivider } from "./ThemeDivider";
import { themeColors } from "@/theme";

type PageHeaderProps = {
  heading?: string;
  background?: string;
  editMode?: boolean;
  backMode?: boolean;
};

const ThemePageHeader = (props: PageHeaderProps) => {
  const { height } = useWindowDimensions();

  return (
    <>
      <View
        className="w-full"
        style={{
          height: height * 0.08,
          backgroundColor: props.background ?? "transparent",
          shadowOpacity: 0.15,
        }}
      >
        <View className="relative">
          <View className="absolute left-5 top-5 items-center justify-center">
            <BackButton goBack />
          </View>
        </View>
        <View className="flex-1 items-center justify-center">
          <ThemeText variant="heading" className="text-xl opacity-55 truncate">
            {props?.heading ? props?.heading : ""}
          </ThemeText>
        </View>
      </View>
      <SectionDivider />
    </>
  );
};

export default ThemePageHeader;
