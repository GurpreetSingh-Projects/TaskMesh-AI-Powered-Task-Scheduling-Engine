import { StyleSheet, Text, View } from "react-native";
import React from "react";
import { ThemeSkeleton } from "@/components/ThemeSkeleton";
import Animated from "react-native-reanimated";
import { themeColors } from "@/theme";

const pulse = { from: { opacity: 0.5 }, to: { opacity: 0.8 } };

const HomePlaceholder = () => {
  return (
    <Animated.View
      style={[
        {
          flex: 1,
          backgroundColor: themeColors?.smoke,
          animationName: pulse,
          animationDuration: 1200,
          animationIterationCount: "infinite",
          animationDirection: "alternate",
          animationTimingFunction: "ease-in-out",
        },
      ]}
    />
  );
};

export default HomePlaceholder;

const styles = StyleSheet.create({});
