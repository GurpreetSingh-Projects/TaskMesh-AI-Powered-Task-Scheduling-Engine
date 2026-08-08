import { View } from "react-native";
import React from "react";
import ThemeText from "./ThemeText";

const OrSeparator = () => {
  return (
    <View className="flex-row w-full items-center justify-center gap-4">
      <View className="flex-1 bg-mist h-px" />
      <View className="h-xl w-xl items-center justify-center text-sm rounded-full border-[0.5px] bg-mist/50 border-mist">
        <ThemeText className="text-sm">or</ThemeText>
      </View>
      <View className="flex-1 bg-mist h-px" />
    </View>
  );
};

export default OrSeparator;
