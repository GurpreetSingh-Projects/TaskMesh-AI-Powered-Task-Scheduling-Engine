import { View } from "react-native";
import React from "react";
import { LinearGradient } from "expo-linear-gradient";

const OnboardingBg = (props) => {
  return (
    <View className={`relative ${props?.className}`}>
      <LinearGradient
        colors={[
          "rgba(255,255,255,1)",
          "rgba(255,255,255,0.35)",
          "rgba(255,255,255,0.0)",
          "rgba(255,255,255,0.35)",
          "rgba(255,255,255,1)",
        ]}
        pointerEvents="none"
        locations={[0, 0.2, 0.5, 0.75, 1]}
        start={{ x: 0.5, y: 0 }}
        end={{ x: 0.5, y: 1 }}
        className="absolute inset-0 "
        style={{ zIndex: 9999 }}
      />
      {props?.children}
    </View>
  );
};

export default OnboardingBg;
